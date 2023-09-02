# Recipe for LibriPhrase <img src="https://img.shields.io/github/license/gusrud1103/LibriPhrase"/></a>
:loudspeaker: [09/02/23] We released an [official test dataset](https://drive.google.com/drive/folders/1pv3wVYzhSwDsL1dIQk93zmFBZg458ujE?usp=share_link) used in our paper. For the fair comparison, you may use this dataset.

## About the dataset
"LibriPhrase" is an open-source dataset tailored for tasks like user-defined keyword spotting (UDKWS), open-vocabulary keyword spotting (OV-KWS), and spoken-term detection (STD). It is constructed based on the LibriSpeech corpus, and we adhere to the license terms of LibriSpeech.

In this recipe, we have taken advantage of exceptional tools and libraries, listed as follows:


* Source : LibriSpeech (ASR corpus) [1]
* Alignment : Montreal Forced Aligner [2][3]
* String distance metric : Levenshtein distance [4]
* Unit : Phoneme-level (extract phoneme information from G2P [5])

### Examples of LibriPhrase
|Anchor text|Easy negative text|Hard negative text|
|----|----|----|
|friend|guard<br/>comfort<br/>superior|frind<br/>rend<br/>trend|
|the river|every morning<br/>town with<br/>not occurred|the giver<br/>the liver<br/>the rigor|
|i mean to|and be made<br/>be a banner<br/>no less than|i seen to<br/>i mean you<br/>we mean to|
|at the right time|began the kissing and<br/>rubbing two bits of<br/>conseil and land spent|at the same time<br/>at the one time<br/>knew the right time|

### Data pipeline
```
./libriphrase.py
./utils.py
./run.sh
./requirements.txt
./data/
  ├── librispeech_clean_dev_all_utt.csv
  ├── ...
  ├── librispeech_other_train_500h_all_utt.csv
  ├── ...
  ├── libriphrase_diffspk_all_1word.csv
  ├── ...
  └── libriphrase_diffspk_all_4word.csv
  
/LibriSpeech_ASR_corpus/
  ├── dev-clean/
  ├── ...
  └── train-other-500/
       ├── BOOKS.TXT
       ├── CHAPTERS.TXT
       ├── ...
       └── train-other-500/
            ├── 1006/
            ├── ...
            └── 985/
                ├── 126224/       
                ├── ...
                └── 126228/
                    ├── 985-126228-0000.wav
                    ...
/LibriPhrase_diffspk_all/
  ├── dev-clean/
  ├── ...
  └── train-other-500/
       └── train-other-500/
            ├── 1006/
            ├── ...
            └── 985/
                ├── 126224/       
                ├── ...
                └── 126228/
                    ├── 985-126228-0004_1word_0.wav
                    ...

```

## Getting started
### Environment
This work is performed in this environment. 
* Python 3.6.9
* Linux Ubuntu 18.04

### 1. Preparation
Before you start, make sure to prepare the [LibriSpeech ASR corpus](https://www.openslr.org/12). <br/>
Once the download is complete, proceed to clone this repository and install the package dependencies using the following steps:

```
git clone https://github.com/gusrud1103/LibriPhrase.git
cd LibriPhrase
pip install -r requirements.txt
```
Afterwards, download alignment CSV files from [Google Link](https://drive.google.com/drive/folders/1wfojzLc_RmYpjKoR89uneZbvSXgDTZDV?usp=sharing) and place the files into ```data``` folder.
```
mkdir data
cd data      # locate CSV files in this folder
```

### 2. Generating LibriPhrase
This recipe is designed to extract short phrases (consisting of 1\~4 words) from the LibriSpeech dataset and organize them into three categories: anchor, positive, and negative. <br/>
By controlling the ```mode``` argument in the script, you can customize the dataset's difficulty (easy/hard) and speaker type (same/different). <br/>
The script will create a hierarchical folder structure based on both the LibriSpeech dataset and manual arguments (Please refer the data pipeline). <br/>

You can use this recipe to generate test dataset. (We will also release the recipe for the training set soon.) <br/>
To ensure a fair comparison with our paper, we offer [the official test dataset](https://drive.google.com/drive/folders/1pv3wVYzhSwDsL1dIQk93zmFBZg458ujE?usp=share_link).  <br/>
We generated the test data from “train-other-500” of LibriSpeech.

```
./run.sh
```
or
```
python3 libriphrase.py --libripath 'your path(librispeech wav files)' --newpath 'new path(libriphrase wav files)' --wordalign './data/librispeech_other_train_500h_all_utt.csv' --output './data/testset_librispeech_other_train_500h_short_phrase.csv' --numpair 3 --maxspk 1611 --maxword 4 --mode 'diffspk_all'
```
#### Arguments
* ```--libripath``` : Folder for LibriSpeech ASR corpus (wav files)
* ```--newpath``` : Folder to save generated LibriPhrase wav files
* ```--wordalign``` : Word alignment information for LibriSpeech ASR corpus (Download csv files to ```data``` folder)
* ```--output``` : Output filename that containing the information about generated LibriPhrase in csv format
* ```--numpair``` : The number of samples in each case 
* ```--maxspk``` : The number of speakers (for reducing computation)
* ```--maxword``` : The maximum number of words to construct short phrase (Select integer from 1 to 4) <br/>
* ```--mode``` : The mode for comparison type (samespk/diffspk denote the consistency of the speaker between anchor and comparison and easy/hard/all denote negative type [```samespk_easy```, ```diffspk_easy```, ```diffspk_hard```, ```diffspk_all```]

### 3. Results
#### Columns:
* ```anchor``` : The file path of the anchor wav file
* ```anchor_spk``` : The speaker of the anchor wav file
* ```anchor_text``` : The text of the anchor wav file
* ```anchor_dur```: The duration of the anchor wav file
* ```comparison```: The file path of the comparison wav file
* ```comparison_spk``` : The speaker of the comparison wav file
* ```comparison_text``` : The text of the comparison wav file
* ```comparison_dur``` : The duration of the comparison wav file
* ```type``` : The category of the comparison (it depends on ```mode```, so if ```mode``` is ```samespk_easy```, then ```samespk_positive```, ```samespk_easyneg``` are showed in the type column.)
>|mode|type category|
>|----|--------|
>|```samespk_easy```|```samespk_positive```, ```samespk_easyneg```|
>|```diffspk_easy```|```diffspk_positive```, ```diffspk_easyneg```|
>|```diffspk_hard```|```diffspk_positive```, ```diffspk_hardneg```|
>|```diffspk_all```|```diffspk_positive```, ```diffspk_easyneg```, ```diffspk_hardneg```|
* ```target``` : If a test sample (comparison) matches with the given anchor (text), the value is ```1```, otherwise ```0```. 
* ```class``` : The number of words in the phrase

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
@inproceedings{Shin22LibriPhrase,
  author={Hyeon-Kyeong Shin and Hyewon Han and Doyeon Kim and Soo-Whan Chung and Hong-Goo Kang},
  title={Learning Audio-Text Agreement for Open-vocabulary Keyword Spotting},
  year=2022,
  booktitle={INTERSPEECH},
  pages={1871--1875},
  doi={10.21437/Interspeech.2022-580}
}
```
