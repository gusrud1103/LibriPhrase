# Recipe for LibriPhrase
### About the dataset
------------
LibriPhrase is an open source dataset for user-defined keyword spotting.
It is derived from LibriSpeech corpus.
##### Examples of LibriPhrase:
|:----|---|---|
|Anchor text| Easy negative text| Hard negative text|
|friend|guard
### Generating LibriPhrase
------------
##### Environment
We work in this environment.
* Python 3.x
* Linux

##### 1. Preparation
Clone and install package dependencies as follows.
```
  git clone https://github.com/gusrud1103/LibriPhrase.git
  pip install -r requirements.txt
```
##### 2. Process
At first, extract short phrase information from LibriSpeech.
Secondly, extract
```
  python3 libriphrase.py --mode 'diffspk_both'
```

##### 3. Results

### Citation
------------
If you use this code, please cite:
```
  @misc{shin2021wake,
    title={},
    }
```
