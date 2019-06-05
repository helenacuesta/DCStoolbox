'''
This script uses pySox to cut all the audio files from a folder given the time boundaries as a csv file.
'''

from utils.data_prep.utils import *
import os
from utils.data_prep import config

filename_dict = create_filename_dictionary(config.channel_assignments)

for filename in os.listdir(config.input_path):

    if 'wav' not in filename: continue

    cut_audiofile_iteratively(filename,config.segment_boundaries,filename_dict)





