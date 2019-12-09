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

def DCS_content_parser(DCS_path='./data/DagstuhlChoirSet/', song_id='*', setting='*', take='*', part='*', mic='*'):
    """Function for parsing dataset content.

    Args:
        DCS_path: Path to Dagstuhl Choir Set
        song_id: Song-ID as specified in publication
        setting: Setting as specified in publication
        take: Take as specified in publication
        part: Part as specified in publication
        mic: Microphone as specified in publication

    Returns:
        Pandas table of found data.
    """
    # check validity of input arguments
    if not os.path.exists(DCS_path):
        raise Error('Invalid path to Dagstuhl Choir Set!')

    if song_id not in ['*', 'DLI', 'DTP', 'DSE']:
        raise Error('Song-ID not valid!')

    if setting not in ['*', 'All', 'QuartetA', 'QuartetB', 'Basses']:
        raise Error('Setting not valid!')

    if part not in ['*', 'S1', 'S2', 'A1', 'A2', 'T1', 'T2', 'B1', 'B2', 'B3', 'B4', 'B5', 'Piano', 'Stereo']:
        raise Error('Part not valid!')

    if mic not in ['*', 'STM', 'STL', 'STR', 'SPL', 'SPR', 'DYN', 'HSM', 'LRX']:
        raise Error('Microphone-ID not valid!')

    # set paths to subfolders ([Name, Path, File-Extension])
    path_spec = np.array([['Audio', DCS_path + 'Audio/norm-downsampled/', 'wav'],
                          ['BeatAnnotation', DCS_path + 'Annotations/beat_alabs/', 'csv'],
                          ['MIDI', DCS_path + 'Annotations/SheetMusic_aligned_AudioLabsBeats/', 'midi'],
                          ['MIDIsoni', DCS_path + 'Annotations/SheetMusic_aligned_AudioLabsBeats/', 'wav'],
                          ['F0CREPE', DCS_path + 'Annotations/pitch/CREPE/', 'csv'],
                          ['F0PYIN', DCS_path + 'Annotations/pitch/PYIN/modified_unvoiced/', 'csv']])

    # initialize new Pandas dataframe
    table_headers = ['Song-ID', 'Setting', 'Take', 'Part', 'Mic']
    table_headers.extend(path_spec[:, 0])
    DCS_table = pd.DataFrame(columns=table_headers)

    # fill DCS_table
    audio_list = glob.glob('%s%s_%s_%s_%s_%s.%s'%(path_spec[0, 1], song_id, setting, take, part, mic, path_spec[0, 2]))

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
        cur_part = tail_s[3]
        cur_mic = tail_s[4]

        # go through available annotations
        for data_idx in range(1, path_spec.shape[0]):
            file_path = '%s%s_%s_%s_%s_%s.%s'%(path_spec[data_idx, 1], cur_song_id, cur_setting, cur_take,
                                               cur_part, cur_mic, path_spec[data_idx, 2])

            if os.path.exists(file_path):
                new_row.append(file_path)
            else:
                # no files found
                new_row.append('')
                continue

        # append row to DCS_table
        DCS_table = DCS_table.append(pd.Series(new_row, index=DCS_table.columns ), ignore_index=True)

    # sort DCS_table
    DCS_table.sort_values(table_headers, inplace=True)
    DCS_table = DCS_table.reset_index(drop=True)

    return DCS_table
