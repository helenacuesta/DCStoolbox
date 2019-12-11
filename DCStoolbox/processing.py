import librosa
import vamp
import numpy as np

def extract_F0_pYIN_vamp(fn, Fs=22050, H=128, N=1024):
    # load wave file
    x, fs = librosa.load(fn, sr=Fs)

    # pYIN parameters
    param = {'threshdistr': 2, 'outputunvoiced': 2, 'precisetime': 0}

    # Options: smoothedpitchtrack, f0candidates, f0probs, voicedprob, candidatesalience, smoothedpitchtrack, notes
    pYIN_note_output = vamp.collect(x, Fs, "pyin:pyin", output='notes', parameters=param, step_size=H, block_size=N)
    pYIN_f0_output = vamp.collect(x, Fs, "pyin:pyin", output='smoothedpitchtrack', parameters=param, step_size=H, block_size=N)

    # reformating
    traj = np.empty((0, 2))
    for entry in pYIN_note_output['list']:
        timestamp = entry['timestamp']
        duration = entry['duration']

        traj = np.vstack((traj, [timestamp, timestamp+duration]))

    return traj
