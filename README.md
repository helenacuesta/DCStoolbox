# Dagstuhl-ChoirSet

This repository contains the code (work in progress) to create the Dagstuhl ChoirSet.

Authors: Sebastian Rosenzweig and Helena Cuesta.

## UTILS

### Data preparation
* beat2measure
* midi2trajectory
* downsampling (pysox)
* normalizing (potentially pysox)
* video-synch (scipy)
* mixing audio files (pysox)
* multi-f0 labels generation
* xml --> midi (CW?)

### Processing
* pYIN Vamp
* Salience function
* Sonification: f0, beat, measure

### Visualization
* f0tools, visualization functions/librosa: beats/measures, f0 activity, f0 trajectories, midi
* jupyter notebook player (SR)
* pypianoroll (?) for MIDI visualization

## EXPERIMENTS
* Experiment1.ipynb
* Experiment2.ipynb

## DATA FILES
(not included in the code repository)

## To run the Jupyter notebooks please
* Install Miniconda
* `conda env create -f environment.yml`
* `source activate choirset`

If you wan to contribute, please install nbstripout:
`nbstripout --install`
