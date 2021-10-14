# Recipe for LibriPhrase <img src="https://img.shields.io/github/license/gusrud1103/LibriPhrase"/></a>
## About the dataset
LibriPhrase is an open source dataset for user-defined keyword spotting.
It is derived from LibriSpeech corpus.
* Source : LibriSpeech (ASR corpus) [1]
* Alignment : Montreal Forced Aligner [2]
* String distance metric : Levenshtein distance [3]
* Unit : Phoneme-level (extract phoneme information from G2P [4])

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
If downloaded complete, clone the repository and install package dependencies as follows.
```
git clone https://github.com/gusrud1103/LibriPhrase.git
pip install -r requirements.txt
```

### 2. Process
At first, extract short phrase(consists of 1~4 words) with wav files from LibriSpeech. <br/>
Secondly, construct anchor, positive, negative for LibriPhrase. <br/>
You can choose negative type(easy, hard) and speaker type(same, different) by adjusting ```mode``` argument. <br/>
#### Arguments
* ```--input``` : file name path
* ```--output``` : 
* ```--mode``` : front part denotes consistency of speaker between anchor and comparison [```samespk_easy```, ```diffspk_easy```, ```diffspk_hard```, ```diffspk_all```]
* ```--numpair``` :
* ```--maxspk``` :
* ```--maxword``` : <br/>
Run the code.
```
python3 libriphrase.py --mode 'diffspk_all'
```

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
[2] Michael McAuliffe, Michaela Socolof,  Sarah  Mihuc,Michael Wagner, and Morgan Sonderegger, “Montreal forced  aligner: Trainable text-speech alignment using kaldi.,” in INTERSPEECH, 2017.<br/>
[3] Vladimir I Levenshtein et al., “Binary codes capable of correcting deletions, insertions, and reversals,” in Soviet physics doklady. Soviet Union, 1966, vol. 10, pp. 707–710.<br/>
[4] Jongseok Park, Kyubyong Kim, “g2pe,”https://github.com/Kyubyong/g2p, 2019.<br/>
## License
Distributed under the MIT License. See ```LICENSE``` for more information.

## Citation
If you use this code, please cite:
```
{}
```
