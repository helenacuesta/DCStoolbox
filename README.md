# Dagstuhl ChoirSet Toolbox

This is the accompanying Python toolbox for the Dagstuhl ChoirSet:

Sebastian Rosenzweig, Helena Cuesta, Christof Weiß, Frank Scherbaum, Emilia Gómez and Meinard Müller. Dagstuhl ChoirSet: A
Multitrack Dataset for MIR Research on Choral Singing. Transactions of the International Society for Music Information Retrieval (TISMIR), 3(1): 98–110, 2020.

## Get started
1. Download the DCS dataset from [Zenodo](https://doi.org/10.5281/zenodo.3897182)
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
* demo1_dataParser.ipynb: Demo of dataset parser.
* demo2_F0Estimation.ipynb: F0-estimation using pYIN and CREPE.

## Evaluation Notebooks
* eval1_F0Annotations.ipynb: Evaluation of automatically extracted F0-trajectories on manual annotations.
