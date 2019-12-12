'''
This scrip max-normalizes audio files and downsamples them (if necessary) to 22050 Hz.
'''

import os
from DCStoolbox.preparation import utils
from DCStoolbox.preparation import config

for filename in os.listdir(config.output_path):

    if not filename.endswith('wav'): continue
    utils.normalize_audio_file(config.output_path, filename)
    print(filename)
