# Recipe for LibriPhrase <img src="https://img.shields.io/github/license/gusrud1103/LibriPhrase"/></a>
## About the dataset
LibriPhrase is an open source dataset for user-defined keyword spotting.
It is derived from LibriSpeech corpus.
* Source : LibriSpeech (ASR corpus) [1]
* Alignment : Montreal Forced Aligner [2][3]
* String distance metric : Levenshtein distance [4]
* Unit : Phoneme-level (extract phoneme information from G2P [5])

### Examples of LibriPhrase:
|Anchor text|Easy negative text|Hard negative text|
|----|----|----|
|friend|guard<br/>comfort<br/>superior|frind<br/>rend<br/>trend|
|the river|every morning<br/>town with<br/>not occurred|the giver<br/>the liver<br/>the rigor|
|i mean to|and be made<br/>be a banner<br/>no less than|i seen to<br/>i mean you<br/>we mean to|
|at the right time|began the kissing and<br/>rubbing two bits of<br/>conseil and land spent|at the same time<br/>at the one time<br/>knew the right time|

## Getting started
### Environment
This work is performed in this environment. 
* Python 3.6.9
* Linux Ubuntu 18.04

### 1. Preparation
Before started, please prepare the [LibriSpeech ASR corpus](https://www.openslr.org/12). <br/>
Also, download alignment csv files from [Google Link](https://drive.google.com/drive/folders/1oUEOmINlwHVrT32b4XxQB3OkyEiL3buh?usp=sharing) and locate the files to data folder.
```
mkdir data
cd data      # locate csv files in this folder
```
If downloaded complete, clone the repository and install package dependencies as follows.
```
git clone https://github.com/gusrud1103/LibriPhrase.git
cd LibriPhrase
pip install -r requirements.txt
```

### 2. Process
At first, it needs to extract short phrase(consists of 1~4 words) from LibriSpeech, and then construct anchor, positive, negative for LibriPhrase. <br/>
Especially, you can choose negative type(easy, hard) and speaker type(same, different) by adjusting ```mode``` argument. <br/>
Finally, it will export wav files for the convenient usage. 
** It takes few days if you use train-other-500.
```
./run.sh
```
or
```
python3 libriphrase.py --input './data/' --output './data/testset_librispeech_other_train_500h_short_phrase.csv' --numpair 3 --maxspk 1611 --maxword 4 --mode 'diffspk_all'
```
#### Arguments
* ```--libriroot``` : original LibriSpeech wav files path
* ```--newroot``` : new short phrase version of LibriSpeech path
* ```--wordalign``` : word alignment information from ```data``` folder
* ```--output``` : LibriPhrase file name with path
* ```--mode``` : front part denotes consistency of speaker between anchor and comparison [```samespk_easy```, ```diffspk_easy```, ```diffspk_hard```, ```diffspk_all```]
* ```--numpair``` : the number of samples in each case 
* ```--maxspk``` : the number of speakers (for reducing computation)
* ```--maxword``` : the maximum number of words to construct short phrase <br/>

### 3. Results
#### Coloums:
* ```anchor``` : the file path of the anchor wav file
* ```anchor_spk``` : the speaker of the anchor wav file
* ```anchor_text``` : the text of the anchor wav file
* ```anchor_dur```: the duration of the anchor wav file
* ```comparison```: the file path of the comparison wav file
* ```comparison_spk``` : the speaker of the comparison wav file
* ```comparison_text``` : the text of the comparison wav file
* ```comparison_dur``` : the duration of the comparison wav file
* ```type``` : the category of the comparison (it depends on ```mode```, so if ```mode``` is ```samespk_easy```, then ```samespk_positive```, ```samespk_easyneg``` are showed in the type column.)
>|mode|type category|
>|----|--------|
>|```samespk_easy```|```samespk_positive```, ```samespk_easyneg```|
>|```diffspk_easy```|```diffspk_positive```, ```diffspk_easyneg```|
>|```diffspk_hard```|```diffspk_positive```, ```diffspk_hardneg```|
>|```diffspk_all```|```diffspk_positive```, ```diffspk_easyneg```, ```diffspk_hardneg```|
* ```target``` : if anchor and comparison is same category, then the value is ```1```, otherwise ```0```.
* ```class``` : the number of words in the phrase

## Reference
[1] Vassil Panayotov, Guoguo Chen, Daniel Povey, and San-jeev Khudanpur, “Librispeech:  an asr corpus based onpublic domain audio books,” in ICASSP, 2015.<br/>
[2] Loren Lugosch, Mirco Ravanelli, Patrick Ignoto, Vikrant Singh Tomar, and Yoshua Bengio, "Speech Model Pre-training for End-to-End Spoken Language Understanding", INTERSPEECH 2019. <br/>
[3] Michael McAuliffe, Michaela Socolof,  Sarah  Mihuc,Michael Wagner, and Morgan Sonderegger, “Montreal forced  aligner: Trainable text-speech alignment using kaldi.,” in INTERSPEECH, 2017.<br/>
[4] Vladimir I Levenshtein et al., “Binary codes capable of correcting deletions, insertions, and reversals,” in Soviet physics doklady. Soviet Union, 1966, vol. 10, pp. 707–710.<br/>
[5] Jongseok Park, Kyubyong Kim, “g2pe,”https://github.com/Kyubyong/g2p, 2019.<br/>
## License
Distributed under the MIT License. See ```LICENSE``` for more information.

## Citation
If you use this code, please cite:
```
@misc{LibriPhrase2021,
  author = {Shin, Hyeon-Kyeong Shin and Han, Hyewon and Kim, Doyeon and Chung, Soo-Whan and Kang, Hong-Goo},
  title = {LibriPhrase},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/gusrud1103/LibriPhrase}}
}
```
