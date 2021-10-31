#!/bin/bash


# construct positive, easy negative, hard negative for LibriPhrase
echo "======================================="
echo "         Construct LibriPhrase         "
echo "======================================="
python3 libriphrase.py --output ./data/testset_librispeech_other_train_500h_short_phrase.csv --numpair 3 --mode diffspk_all

