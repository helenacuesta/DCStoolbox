'''
This script uses pySox to cut all the audio files from a folder given the time boundaries as a csv file.
'''

import sox
import pandas as pd
import numpy as np

def cut_audio_iteratively(input_file,bounds,output_path):

    cnt=0
    for line in bounds:

        cnt+=1
        tin,tout = line[0],line[1]

        tfm = sox.Transformer()
        tfm.trim(tin,tout)
        output_file = output_path + '{}_{}_{}_{}.wav'.format(line[2],line[3],line[4],line[5])

        tfm.build(input_file,output_file)

        print(cnt)


def read_time_boundaries(csvfile):

    bounds = np.array(pd.read_csv(csvfile))

    return bounds

### Calling stuff here

bounds_file = '../cut_annotations_v1.csv'
audio_file = '../audioInput/Dagstuhl_Stereo.wav'

bounds = read_time_boundaries(bounds_file)

cut_audio_iteratively(audio_file,bounds,'../audioOutput/')





