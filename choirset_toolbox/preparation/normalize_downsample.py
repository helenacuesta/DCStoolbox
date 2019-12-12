'''
This scrip max-normalizes audio files and downsamples them (if necessary) to 22050 Hz.
'''

import os
from choirset_toolbox.preparation import utils
from choirset_toolbox.preparation import config

for filename in os.listdir(config.output_path):

    if not filename.endswith('wav'): continue
    utils.normalize_audio_file(config.output_path, filename)
    print(filename)
