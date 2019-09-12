'''
This script takes time annotations from Sonic Visualiser and converts them to the format:

t_in, t_out, label (given by SV)

We assume each line of the csv contains one time instant and therefore two consecutive lines represent a segment

Example file format:

0.000000000,2.1
14.537645833,2.2
27.290041667,2.3
33.228708333,2.4
45.363000000,3.1
51.893791667,3.2
64.284500000,3.3
68.581625000,3.4
80.421541667,4.1
83.958708333,4.2


Command to execute the script should be: python3 annot2bounds.py path_to_the_annotation_file annotation_filename output_filename

'''

import pandas as pd
import numpy as np
import sys


#PATH = '../'
#FILENAME = 'dagstuhl_take_boundaries.csv'

def main(PATH, FILENAME, OUTPUT_FILENAME):

    input_data = np.array(pd.read_csv(PATH+FILENAME))

    output_data = []
    for i in np.arange(input_data.shape[0]-1,step=2):

        tin = input_data[i,0]
        tout = input_data[i+1,0]
        output_data.append(
            np.array([
                tin,tout,input_data[i,1]
            ]))

    pd.DataFrame(output_data).to_csv(PATH+'v1_'+OUTPUT_FILENAME)


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("Input arguments missing.")
    else:
        path = sys.argv[1]
        filename = sys.argv[2]
        out_filename = sys.argv[3]

        main(path, filename, out_filename)








