# script to convert alabs beat annotations to measure annotations

import pandas as pd
import glob
import os
import numpy as np

beat_anno_path = '../../data/2019_DagstuhlRecording/Dagstuhl Dataset/Annotations/beat_alabs/'
measure_anno_path = '../../data/2019_DagstuhlRecording/Dagstuhl Dataset/Annotations/measure_alabs/'

file_list = glob.glob(beat_anno_path + '*.csv')

for file in file_list:
    print(file)

    # load annotation
    annotation = pd.read_csv(file, header=None)

    # find measure starts (include last entry corresponding end of audio file)
    measure_start = (annotation[1] - np.floor(annotation[1])) == 0
    measure_start.iloc[-1] = True
    m_anno = annotation[measure_start].reset_index(drop=True)
    #m_anno[1] = np.arange(1, len(m_anno)+1).astype(int)
    #m_anno[1].iloc[-1] += 0.999

    # write out new annotation file
    out_name = os.path.basename(file)
    out_name = out_name.replace('beat', 'measure')

    m_anno.to_csv(measure_anno_path + out_name, float_format='%.3f', header=None, index=False)
