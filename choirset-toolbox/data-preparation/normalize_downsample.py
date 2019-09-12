'''
This scrip uses PySox to normalize audiofiles in a folder to -2dB and downsample them (if necessary) to 22050 Hz.
'''

import utils
import os
from utils.data_prep import config

for filename in os.listdir(config.output_path):

    if not filename.endswith('wav'): continue
    utils.normalize_audio_file(config.output_path, filename)
    print(filename)
