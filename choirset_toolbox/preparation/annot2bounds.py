'''
This script takes time annotations from Sonic Visualiser and converts them to the format:

t_in, t_out, label (given by SV)

The  input annotations define the segments to be cut from a full audio recording, and they
contain timestamps where a new segment starts or ends. We assume each line of the csv contains one time instant and
therefore two consecutive lines represent a segment

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

import argparse


def main(args):

    input_data = np.array(pd.read_csv(args.PATH+args.FILENAME))

    output_data = []
    for i in np.arange(input_data.shape[0]-1, step=2):

        tin = input_data[i,0]
        tout = input_data[i+1,0]
        output_data.append(
            np.array([
                tin,tout,input_data[i,1]
            ]))

    pd.DataFrame(output_data).to_csv(args.PATH+'v1_'+args.OUTPUT_FILENAME)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Convert timestamp segment annotations to segment boundaries, i.e. [t_start, t_end, label]")

    parser.add_argument("--folder",
                        dest="PATH",
                        type=str,
                        help="Path to the folder of the annotation file.")
    parser.add_argument("--filename",
                        dest="FILENAME",
                        type=str,
                        help="Filename of the annotation file."
                        )
    parser.add_argument("--out_fname",
                        dest="OUTPUT_FILENAME",
                        type=str,
                        help="Filename to export the new annotation file.")

    main((parser.parse_args()))








