"""
Functions for F0 estimation: pYIN (Mauch and Dixon, 2014) and CREPE (Kim et al. 2018)
Author: Sebastian Rosenzweig, Helena Cuesta
License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License


To run this code one needs to:

- Install the pYIN  Vamp Plug-in (https://code.soundsoftware.ac.uk/projects/pyin/files) following
these instructions: http://www.vamp-plugins.org/download.html#install
- Then, to use the pYIN Vamp, install the Vamp Python package: https://pypi.org/project/vamp/.

This file is part of the Dagstuhl Choir Set Toolbox (https://github.com/helenacuesta/ChoirSet-Toolbox).
"""

import crepe
import vamp

import librosa
import numpy as np
import pandas as pd

import os
import argparse

def extract_F0_pYIN_vamp(folder, fn, sr=22050, H=221, N=2048):

    ''' Given an audio file, use the pYIN Vamp Plug-in to extract the F0
        and the confidence of each frame to be voiced.
    '''

    # load wave file
    x, fs = librosa.load(os.path.join(folder, fn), sr=sr)

    # pYIN parameters
    param = {'threshdistr': 2, 'outputunvoiced': 2, 'precisetime': 0}

    '''
    outputs:
    'voicedprob' outputs the probability of each frame to be voiced
    'smoothedpitchtrack' outputs the smoothed pitch track
    parameters:
    'outputunvoiced': 0 (No), 1 (Yes as zeros), 2 (Yes as negative frequencies)
    '''

    pYIN_f0_output = vamp.collect(x, sr, "pyin:pyin", output='smoothedpitchtrack', parameters=param, step_size=H,
                                  block_size=N)['vector']

    pYIN_voiced_prob = vamp.collect(x, sr, "pyin:pyin", output='voicedprob', parameters=param, step_size=H,
                                  block_size=N)['vector']

    time_step = float(pYIN_f0_output[0])
    F0 = pYIN_f0_output[1]
    voiced_prob = pYIN_voiced_prob[1]
    timestamp = np.arange(start=0, stop=(len(F0)-0.5)*time_step, step=time_step)#[:-1]


    traj = np.vstack([timestamp, F0, voiced_prob]).transpose()

    if not os.path.exists(os.path.join(folder, 'pYIN')):
        os.mkdir(os.path.join(folder, 'pYIN'))

    pd.DataFrame(traj).to_csv(os.path.join(folder, 'pYIN', fn[:-3] + 'csv'), header=None)
    print("{} F0 curve saved to {}".format(fn, os.path.join(folder, 'pYIN', fn[:-3] + 'csv')))

    return traj


def extract_F0_CREPE(folder, fn, sr=22050):

    '''Given an audio file, use the CREPE method to extract the F0
        and the confidence of each frame. The 'model_capacity' parameter is set
        to "full" by default, but can be one of these: tiny|small|medium|large|full
    '''

    x, sr = librosa.load(os.path.join(folder, fn), sr=sr)
    timestamp, F0, confidence, _ = crepe.predict(x, sr, model_capacity='full', viterbi=True)

    traj = np.vstack([timestamp, F0, confidence]).transpose()

    if not os.path.exists(os.path.join(folder, 'CREPE')):
        os.mkdir(os.path.join(folder, 'CREPE'))

    pd.DataFrame(traj).to_csv(os.path.join(folder, 'CREPE', fn[:-3] + 'csv'), header=None)
    print("{} F0 curve saved to {}".format(fn, os.path.join(folder, 'CREPE', fn[:-3] + 'csv')))

    return traj



def main(args):

    # single audio file
    if args.mode == 1:
        if args.method == 'pYIN':
            pyin_traj = extract_F0_pYIN_vamp(args.audio_folder, args.audio_file)
        elif args.method == 'crepe':
            crepe_traj = extract_F0_CREPE(args.audio_folder, args.audio_file)
        else:
            print("F0 estimation method not found. Please select a valid method: pYIN or CREPE.")

    # folder with several files
    elif args.mode == 2:
        for fn in os.listdir(args.audio_folder):
            if not fn.endswith('wav'): continue

            if args.method == 'pYIN':
                pyin_traj = extract_F0_pYIN_vamp(args.audio_folder, fn)
            elif args.method == 'crepe':
                crepe_traj = extract_F0_CREPE(args.audio_folder, fn)
            else:
                print("F0 estimation method not found. Please select a valid method: pYIN or CREPE.")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Use pYIN or CREPE to extract F0 from an audio signal. The user can either specify the path of "
                    "a single audio file or provide the path to a folder with several audio files."
    )

    parser.add_argument('--method',
                        dest='method',
                        type=str,
                        help='F0 estimation method (pYIN/crepe)')
    parser.add_argument('--mode',
                        dest='mode',
                        type=int,
                        help='Mode is 1 for a single audio file and 2 for a folder with several files.')
    parser.add_argument('--folder',
                        dest='audio_folder',
                        type=str,
                        help='Path to the folder with the audio file(s).')
    parser.add_argument('--audio_file',
                        dest='audio_file',
                        type=str,
                        help='If mode=1, this parameter should be the filename.')


    main(parser.parse_args())
