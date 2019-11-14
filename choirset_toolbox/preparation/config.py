import pandas as pd
import numpy as np


input_path = "../audioInput/"
#output_path = "../audioOutput/"
output_path = "/Volumes/MTG MIR/DagstuhlChoirDataset/"

boundaries_file = "../cut_annotations.csv"
channels_file = "../channel_assignments.csv"

output_folder_downsampled = "../audioOutput/downsampled/"

channel_assignments = np.array(pd.read_csv(channels_file))  # channel assignment
segment_boundaries = np.array(pd.read_csv(boundaries_file))   # time boundaries of the segments to cut

