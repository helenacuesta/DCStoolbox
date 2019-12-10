"""
Main parsing functions.
Author: Sebastian Rosenzweig, Helena Cuesta
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

This file is part of the Dagstuhl Choir Set Toolbox (https://github.com/helenacuesta/ChoirSet-Toolbox).
"""

import glob
import numpy as np
import os
import pandas as pd

class Error(Exception):
    """Simple error class"""
    pass

def DCS_content_parser(DCS_path='./data/DagstuhlChoirSet/', song_id='*', setting='*', take='*', section='*', mic='*'):
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

    if song_id not in ['*', 'DLI', 'DTP', 'DSE']:
        raise Error('Song-ID not valid!')

    if setting not in ['*', 'All', 'QuartetA', 'QuartetB', 'Basses']:
        raise Error('Setting-ID not valid!')

    section_list = ['Stereo', 'S1', 'S2', 'A1', 'A2', 'T1', 'T2', 'B1', 'B2', 'B3', 'B4', 'B5', 'Piano', '*']
    if section not in section_list:
        raise Error('Section-ID not valid!')

    if mic not in ['*', 'STM', 'STL', 'STR', 'SPL', 'SPR', 'DYN', 'HSM', 'LRX']:
        raise Error('Microphone-ID not valid!')

    # set paths to subfolders ([Name, Path, Suffix, File-Extension])
    path_spec = np.array([['Audio', DCS_path + 'Audio/norm-downsampled/', '', 'wav'],
                          ['BeatAnnotation', DCS_path + 'Annotations/beat_alabs/', '_beatAnnotations', 'csv'],
                          ['MIDI', DCS_path + 'Annotations/SheetMusic_aligned_AudioLabsBeats/', '', 'midi'],
                          ['MIDIsoni', DCS_path + 'Annotations/SheetMusic_aligned_AudioLabsBeats/', '','wav'],
                          ['F0CREPE', DCS_path + 'Annotations/pitch/CREPE/', '', 'csv'],
                          ['F0PYIN', DCS_path + 'Annotations/pitch/PYIN/modified_unvoiced/', '', 'csv']])

    # initialize new Pandas dataframe
    table_headers = ['Song-ID', 'Setting', 'Take', 'Section', 'Microphone']
    table_headers.extend(path_spec[:, 0])
    DCS_table = pd.DataFrame(columns=table_headers)

    # fill DCS_table
    audio_list = glob.glob('%s%s_%s_%s_%s_%s%s.%s'%(path_spec[0, 1], song_id, setting, take, section, mic, path_spec[0, 2],
                                                    path_spec[0, 3]))

    for audio_file in audio_list:
        new_row = []

        # fill first five columns
        head, tail = os.path.split(audio_file)
        tail_s = tail[:-4].split('_')
        new_row.extend(tail_s)
        new_row.append(audio_file)

        cur_song_id = tail_s[0]
        cur_setting = tail_s[1]
        cur_take = tail_s[2]
        cur_section = tail_s[3]
        cur_mic = tail_s[4]

        # go through available annotations
        for data_idx in range(1, path_spec.shape[0]):
            file_path = '%s%s_%s_%s_%s_%s%s.%s'%(path_spec[data_idx, 1], cur_song_id, cur_setting, cur_take,
                                                 cur_section, cur_mic, path_spec[data_idx, 2], path_spec[data_idx, 3])

            if os.path.exists(file_path):
                new_row.append(file_path)
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
