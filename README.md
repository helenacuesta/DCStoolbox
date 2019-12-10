# Dagstuhl Choir Set Toolbox

A Python toolbox for using the CSD dataset (work in progress).

Authors: Sebastian Rosenzweig and Helena Cuesta.

## Get started
1. Download the dataset from [Zenodo](https://www.zenodo.org)
2. Clone repository
  * `git pull https://github.com/helenacuesta/ChoirSet-Toolbox.git`
  * `git submodule init`
  * `git submodule update`
3. Install Miniconda
  * `cd ./CSD-toolbox`
  * `conda env create -f environment.yml`
  * `source activate choirset`
  
To use the toolbox functions type:
`import CSD-toolbox`

If you want to contribute to this repository, please install nbstripout:
`nbstripout --install`

## Demo Notebooks
* demo1_dataVisualization.ipynb: Basic parsing, visualization, and sonification
* Microphone comparison.ipynb
* Intonation quality.ipynb
* Singer evolution or basses analysis.ipynb

### Data preparation
* utils.py: Functions for syncing audio and video
* downsampling 
* normalizing 
* video-synch 
* audio to MIDI alignment

### Data processing
Python file (data_processing.py) with all functions to process data. Probably including:

* Reading annotations (csv files)
* pYIN Vamp (?)
* beat2measure
* midi2trajectory
* mixing audio files
* Sonification: f0, beat, measure

### Visualization
Python file (visualization.py) with functions to visualize data. Probably including:

* f0tools, visualization functions/librosa: beats/measures, f0 activity, f0 trajectories, midi
* jupyter notebook player (SR)
* MIDI visualization (from CSV files [onset, offset, pitch])
