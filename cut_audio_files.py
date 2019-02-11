'''
This script uses pySox to cut all the audio files from a folder given the time boundaries as a csv file.
'''

import sox
import pandas as pd

def cut_audio(input_file,output_file,tin,tout):

    tfm = sox.Transformer()
    tfm.trim(tin,tout)
    # create the output file.
    tfm.build(input_file, 'path/to/output/audio.aiff')



