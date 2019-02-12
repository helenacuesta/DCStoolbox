'''
This script uses pySox to cut all the audio files from a folder given the time boundaries as a csv file.
'''

from utils import *
import os
import config

'''
def cut_audiofile_iteratively(input_file,bounds,output_path):

    cnt=0
    # cut one segment of the input audio at each iteration of the for loop
    for line in bounds:

        cnt+=1
        # define time boundaries of each segment
        tin,tout = line[0],line[1]

        tfm = sox.Transformer()
        tfm.trim(tin,tout)

        #output_file = output_path + '{}_{}_{}_{}.wav'.format(line[2],line[3],line[4],line[5])

        # TODO: we need to define how to name the files automatically given the csv files with annotations
        output_file = ''

        tfm.build(input_file,output_file)

        print(cnt)


def read_time_boundaries(csvfile):

    bounds = np.array(pd.read_csv(csvfile))

    return bounds

'''

filename_dict = create_filename_dictionary(config.channel_assignments)

for filename in os.listdir(config.input_path):

    if 'wav' not in filename: continue

    cut_audiofile_iteratively(filename,config.segment_boundaries,filename_dict)





