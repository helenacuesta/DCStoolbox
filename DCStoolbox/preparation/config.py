import pandas as pd
import numpy as np
import os

input_path = "/home/helenacuesta/Desktop/MTG/Data/DagstuhlOriginalStems/"
#output_path = "../audioOutput/"
output_path = "/home/helenacuesta/Desktop/MTG/Data/DagstuhlChoirSetNewCuts/"

boundaries_file = "../../../cut_annotations_final.csv"
channels_file = "../../../channel_assignments.csv"

output_folder_downsampled = os.path.join(output_path, "norm_downsampled/")

channel_assignments = np.array(pd.read_csv(channels_file))  # channel assignment
segment_boundaries = np.array(pd.read_csv(boundaries_file))   # time boundaries of the segments to cut

