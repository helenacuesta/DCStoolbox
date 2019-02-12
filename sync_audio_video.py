'''
This script uses ffmpeg and scipy crosscorrelation to sync and cut videos with audio recordings
'''

import pandas as pd
import glob
import librosa
import scipy.signal
import numpy as np
import ffmpeg
import os
import subprocess

# set paths
video_path = './data/'
audio_ref_path = './audio_ref.wav'  # e.g. the stereo mix
cut_anno_path = './Cut Annotations.csv'
output_anno_path = './detected_video_positions.csv'

fs = 11025  # low fs sufficient

# load files
cut_anno = pd.read_csv(cut_anno_path)
cut_anno = cut_anno[~cut_anno['Song ID'].isin(['DSE'])]  # remove all DSE entries from list, since we do not want to sync them
audio_ref, _ = librosa.load(audio_ref_path, sr=fs, mono=True)
file_list = glob.glob(video_path + '*.mov') + glob.glob(video_path + '*.mp4') + glob.glob(video_path + '*.MOV')


def compute_sync_lag(s1, s2):
    # compute cross correlation (symmetric)
    cc = scipy.signal.correlate(s1, s2, mode='full', method='fft')

    delay = np.abs(cc).argmax() - len(s2) + 1

    return delay.astype(int)


def extract_audio_from_video(video, fs):
    command = ffmpeg.input(video)
    command = ffmpeg.output(command, "temp.wav")
    ffmpeg.run(command)

    video_audio, _ = librosa.load('temp.wav', sr=fs)
    os.remove('temp.wav')

    return video_audio


def cut_and_save_video(video, start, duration, output_path):
    video_path = os.path.abspath(output_path + os.path.basename(video))
    command = "ffmpeg -ss " + str(start) + " -i " + os.path.abspath(video) + " -c copy -t " + str(duration) + " " + video_path

    subprocess.call(command, shell=True)


# loop through all video files available
for video_file in file_list:
    print('Current file: ' + video_file)

    # extract video audio
    video_audio = extract_audio_from_video(video_file, fs)

    # compute crosscorrelation with referencedata
    lag = compute_sync_lag(audio_ref, video_audio)
    start_time_s = lag/fs
    end_time_s = (lag + len(video_audio))/fs

    # cut video according to cut annotation
    cut_anno_sorted =  cut_anno.iloc[(cut_anno['Start Time (sec)'] - start_time_s).abs().argsort()].to_numpy()  # find closest value to calculated lag
    actual_start_s = cut_anno_sorted[0, 0]
    actual_end_s = cut_anno_sorted[0, 1]
    cut_start_s = actual_start_s - start_time_s
    cut_end_s = actual_end_s - start_time_s

    cut_and_save_video(video_file, cut_start_s, cut_end_s-cut_start_s, './output/')


    # save annotation
    pd.DataFrame([os.path.basename(video_file), start_time_s, end_time_s]).T.to_csv(output_anno_path, header=False, mode='a', index=False)
