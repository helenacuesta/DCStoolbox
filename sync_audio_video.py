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
from multiprocessing import Pool
import time

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
    time_ms = int(round(time.time() * 1000))
    command = ffmpeg.input(video)
    command = ffmpeg.output(command, str(time_ms) + '.wav')
    ffmpeg.run(command)

    video_audio, _ = librosa.load(str(time_ms) +'.wav', sr=fs)
    os.remove(str(time_ms) + '.wav')

    return video_audio


def cut_and_save_video(video, start, duration, output_file):
    command = "ffmpeg -ss " + str(start) + " -i " + os.path.abspath(video) + " -vcodec libx264 -t " + str(duration) + " " + output_file

    subprocess.call(command, shell=True)


# loop through all video files available
def processing_wrapper(video_file):
    print('Current file: ' + video_file)

    # extract video audio
    video_audio = extract_audio_from_video(video_file, fs)

    # compute crosscorrelation with reference audio
    lag = compute_sync_lag(audio_ref, video_audio)
    start_ref_s = lag/fs  # start in reference audio
    end_ref_s = (lag + len(video_audio))/fs  # end in reference audio

    # cut video according to cut annotation
    # loop through whole video and find all cutpoints
    search_start_s = start_ref_s
    while 1:
        cut_anno_sorted = cut_anno.iloc[(cut_anno['Start Time (sec)'] - search_start_s).abs().argsort()].to_numpy()  # find closest value to calculated lag
        actual_start_s = cut_anno_sorted[0, 0]
        actual_end_s = cut_anno_sorted[0, 1]

        cut_start_s = actual_start_s - start_ref_s
        cut_end_s = actual_end_s - start_ref_s

        if cut_end_s > len(video_audio)/fs:
            # break if snippet is not fully contained in video file
            break

        cur_out_file = './output/' + cut_anno_sorted[0, 2] + '_' + cut_anno_sorted[0, 3] + '_' + cut_anno_sorted[0, 4] + '_SATB_Video.mp4'
        cut_and_save_video(video_file, cut_start_s, cut_end_s-cut_start_s, cur_out_file)

        # save annotation
        pd.DataFrame([os.path.basename(video_file), start_ref_s, end_ref_s]).T.to_csv(output_anno_path, header=False, mode='a', index=False)

        search_start_s = actual_end_s

p = Pool(processes=None)
p.map(processing_wrapper, np.sort(file_list))
