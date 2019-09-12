# Dagstuhl-ChoirSet

This repository contains the code (work in progress) to create the Dagstuhl ChoirSet.

Authors: Sebastian Rosenzweig and Helena Cuesta.

## To run the code:
* Install Miniconda
* `conda env create -f environment.yml`
* `source activate choirset`

If you wan to contribute, please install nbstripout:
`nbstripout --install`

## Demo Notebooks
* Data preparation.ipynb
* Microphone comparison.ipynb
* Intonation quality.ipynb
* Singer evolution or basses analysis.ipynb

## Data files
Not included in the code repository, Zenodo link.

## ChoirSet-Toolbox

To use the toolbox functions type:
`import choirset-toolbox`

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
