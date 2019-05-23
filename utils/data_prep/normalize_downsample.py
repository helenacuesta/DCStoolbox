import utils
import os
import config

for filename in os.listdir(config.output_path):

    if not filename.endswith('wav'): continue
    utils.normalize_audio_file(config.output_path, filename)
    print(filename)
