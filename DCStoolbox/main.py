"""
Main parsing functions.
Author: Helena Cuesta, Sebastian Rosenzweig
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

This file is part of the Dagstuhl ChoirSet Toolbox (https://github.com/helenacuesta/DCStoolbox).
"""

import glob
import numpy as np
import os
import pandas as pd

class Error(Exception):
    """Simple error class"""
    pass

def DCS_content_parser(DCS_path='./DagstuhlChoirSet_V1.0/', song_id='*', setting='*', take='*', section='*', mic='*'):
    """Function for parsing dataset content.

    Args:
        DCS_path: Path to Dagstuhl Choir Set
        song_id: Song-ID as specified in publication
        setting: Setting-ID as specified in publication
        take: Take-ID as specified in publication
        section: Section-ID as specified in publication
        mic: Microphone-ID as specified in publication

    Returns:
        Pandas table of found data.
    """
    # check validity of input arguments
    if not os.path.exists(DCS_path):
        raise Error('Invalid path to Dagstuhl Choir Set!')

    if song_id not in ['*', 'DCS_LI', 'DCS_TP', 'DCS_SE']:
        raise Error('Song-ID not valid!')

    if setting not in ['*', 'FullChoir', 'QuartetA', 'QuartetB', 'Basses']:
        raise Error('Setting-ID not valid!')

    section_list = ['Stereo', 'StereoReverb', 'S1', 'S2', 'A1', 'A2', 'T1', 'T2', 'B1', 'B2', 'B3', 'B4', 'B5', 'Piano', '*']
    if section not in section_list:
        raise Error('Section-ID not valid!')

    if mic not in ['*', 'STM', 'STL', 'STR', 'SPL', 'SPR', 'DYN', 'HSM', 'LRX']:
        raise Error('Microphone-ID not valid!')

    # set paths to subfolders ([Name, Path, File-Extension])
    path_spec = np.array([['Audio', DCS_path + 'audio_wav_22050_mono/', 'wav'],
                          ['Beat', DCS_path + 'annotations_csv_beat/', 'csv'],
                          ['ScoreRepr', DCS_path + 'annotations_csv_scorerepresentation/', 'csv'],
                          ['F0CREPE', DCS_path + 'annotations_csv_F0_CREPE/', 'csv'],
                          ['F0PYIN', DCS_path + 'annotations_csv_F0_PYIN/', 'csv'],
                          ['F0Manual', DCS_path + 'annotations_csv_F0_manual/', 'csv']])

    # initialize new Pandas dataframe
    table_headers = ['Dataset-ID', 'Song-ID', 'Setting', 'Take', 'Section', 'Microphone']
    table_headers.extend(path_spec[:, 0])
    DCS_table = pd.DataFrame(columns=table_headers)

    # fill DCS_table
    audio_list = glob.glob('%s%s_%s_%s_%s_%s.%s'%(path_spec[0, 1], song_id, setting, take, section, mic, path_spec[0, 2]))

    for audio_file in audio_list:
        new_row = []

        # fill first five columns
        head, tail = os.path.split(audio_file)
        tail_s = tail[:-4].split('_')
        new_row.extend(tail_s)
        new_row.append(audio_file)

        cur_dataset_id = tail_s[0]
        cur_song_id = tail_s[1]
        cur_setting = tail_s[2]
        cur_take = tail_s[3]
        cur_section = tail_s[4]
        cur_mic = tail_s[5]

        # go through available annotations
        for data_idx in range(1, path_spec.shape[0]):
            file_path = '%s%s_%s_%s_%s_%s_%s*.%s'%(path_spec[data_idx, 1], cur_dataset_id, cur_song_id, cur_setting, cur_take,
                                                   cur_section, cur_mic, path_spec[data_idx, 2])
            file_list = glob.glob(file_path)

            if file_list:
                if len(file_list) == 1:
                    new_row.append(file_list[0])
                else:
                    new_row.append(tuple(file_list))
            else:
                # no files found
                new_row.append('')
                continue

        # add row to DCS_table
        DCS_table = DCS_table.append(pd.Series(new_row, index=DCS_table.columns), ignore_index=True)

    # sort DCS_table
    DCS_table.sort_values(table_headers, inplace=True)
    DCS_table.Section = DCS_table.Section.astype("category")
    DCS_table.Section.cat.set_categories(section_list, inplace=True)
    DCS_table = DCS_table.sort_values(["Section"]).reset_index(drop=True)

    return DCS_table


def read_csv(fn, header=None, names=None):
    """Reads a CSV file

    Args:
        fn: Filename
        header: Boolean
        names: Column names

    Returns:
        df: Pandas DataFrame
    """
    df = pd.read_csv(fn, sep=',', keep_default_na=False, header=header, names=names)

    return df


def sonify_trajectory_with_sinusoid(traj, audio_len, Fs=22050, amplitude=0.3, smooth_len=11):
    """Sonification of trajectory with sinusoidal
    This function is part of the FMP Notebooks (https://www.audiolabs-erlangen.de/FMP).
    Notebook: C8/C8S2_FundFreqTracking.ipynb

    Args:
        traj: F0 trajectory (time in seconds, frequency in Hz)
        audio_len_samples: Desired audio length in samples
        Fs: Sampling rate
        sine_len: Length of sinusoidal components in sample (hop size)
        smooth_len: Length of amplitude smoothing filter

    Returns:
        x_soni: Sonification
    """
    # unit confidence if not specified
    if traj.shape[1] < 3:
        confidence = np.zeros(traj.shape[0])
        confidence[traj[:,1] > 0] = amplitude
    else:
        confidence = traj[:, 2]

    # initialize
    x_soni = np.zeros(audio_len)
    amplitude_mod = np.zeros(audio_len)

    # Computation of hop size
    #sine_len = int(2 ** np.round(np.log(traj[1, 0]*Fs)/np.log(2)))
    sine_len = int(traj[1, 0]*Fs)

    t = np.arange(0, sine_len)/Fs
    phase = 0

    # loop over all F0 values, insure continuous phase
    for idx in np.arange(0, traj.shape[0]):
        cur_f = traj[idx, 1]
        cur_amp = confidence[idx]

        if cur_f == 0:
            phase = 0
            continue

        cur_soni = np.sin(2*np.pi*(cur_f*t+phase))
        diff = np.maximum(0, (idx+1)*sine_len - len(x_soni))
        if diff > 0:
            x_soni[idx * sine_len:(idx + 1) * sine_len - diff] = cur_soni[:-diff]
            amplitude_mod[idx * sine_len:(idx + 1) * sine_len - diff] = cur_amp
        else:
            x_soni[idx*sine_len:(idx+1)*sine_len-diff] = cur_soni
            amplitude_mod[idx*sine_len:(idx+1)*sine_len-diff] = cur_amp

        phase += cur_f*sine_len/Fs
        phase -= 2*np.round(phase/2)

    # filter amplitudes to avoid transients
    amplitude_mod = np.convolve(amplitude_mod, np.hanning(smooth_len)/np.sum(np.hanning(smooth_len)), 'same')
    x_soni = x_soni * amplitude_mod
    return x_soni


def sonify_score_representation_with_sinusoidals(fns_score, Fs, audio_len_samples):
    """Sonification of score representation

    Args:
        fns_score: Tuple of paths to score representation files
        Fs: Sampling rate
        audio_len_samples: Desired audio length in samples

    Returns:
        x_soni: Sonification
    """
    H = 256
    t = np.arange(0, audio_len_samples/Fs, H/Fs)
    x_soni = np.zeros(audio_len_samples)

    for fn in fns_score:
        score_rep = read_csv(fn, header=None).values

        traj = np.hstack((t.reshape(-1, 1), np.zeros(len(t)).reshape(-1,1)))

        for row in score_rep:
            # get indices of trajectory
            t_start_idx = np.argmin(np.abs(t - row[0]))
            t_end_idx = np.argmin(np.abs(t - row[1]))
            note_len_idx = t_end_idx - t_start_idx

            f_hz = 440 * 2 ** ((row[2]-69)/12)
            traj[t_start_idx:t_end_idx, 1] = [f_hz]*note_len_idx

        x_soni += sonify_trajectory_with_sinusoid(traj, audio_len_samples, Fs=Fs, amplitude=0.3, smooth_len=11)

    return x_soni
