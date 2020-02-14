# Dagstuhl ChoirSet Toolbox

Python toolbox for using DCS dataset.

Blind authors.

## Get started
1. Download the DCS dataset from [Zenodo](https://www.zenodo.org)
2. Clone repository
  * `git pull _hidden URL_
  * `cd ./DCStoolbox`
  * `git submodule init`
  * `git submodule update`
3. Install Miniconda
  * `conda env create -f environment.yml`
  * `source activate DCS`

To use the toolbox functions type:
`import DCStoolbox`

If you want to contribute to this repository, please install nbstripout:
`nbstripout --install`

## Demo Notebooks
* demo1_dataVisualization.ipynb: Basic parsing, visualization, and sonification functions.
* demo2_F0Estimation.ipynb: F0-estimation using pYIN and CREPE.
