# Recipe for LibriPhrase <img src="https://img.shields.io/github/license/gusrud1103/LibriPhrase"/></a>
## About the dataset
LibriPhrase is an open source dataset for user-defined keyword spotting.
It is derived from LibriSpeech corpus.
### Examples of LibriPhrase:
|Anchor text|Easy negative text|Hard negative text|
|----|----|----|
|friend|guard<br/>comfort<br/>superior|frind<br/>rend<br/>trend|
|the river|every morning<br/>town with<br/>not occurred|the giver<br/>the liver<br/>the rigor|
|i mean to|and be made<br/>be a banner<br/>no less than|i seen to<br/>i mean you<br/>we mean to|
|at the right time|began the kissing and<br/>rubbing two bits of<br/>conseil and land spent|at the same time<br/>at the one time<br/>knew the right time|
## Generating LibriPhrase
### Environment
We work in this environment. 
* Python 3.x
* Linux Ubuntu 18.04

### 1. Preparation
Clone and install package dependencies as follows.
```
git clone https://github.com/gusrud1103/LibriPhrase.git
pip install -r requirements.txt
```
### 2. Process
At first, extract short phrase information from LibriSpeech.
Secondly, extract
```
python3 libriphrase.py --mode 'diffspk_both'
```

### 3. Results

## Citation
If you use this code, please cite:
```
  @misc{shin2021wake,
    title={},
    }
```
