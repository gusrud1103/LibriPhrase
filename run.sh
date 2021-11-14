#!/bin/bash


# construct positive, easy negative, hard negative for LibriPhrase
echo "======================================="
echo "         Construct LibriPhrase         "
echo "======================================="

# diffspk_all mode
python3 libriphrase.py  \
--libripath /home/hkshin/server_hdd/Database/LibriSpeech_clean_wav/  \
--newpath /home/hkshin/server_hdd/Database/LibriPhrase_diffspk_all/  \
--wordalign ./data/librispeech_other_train_500h_all_utt.csv  \
--output ./data/libriphrase_diffspk_all.csv  \
--numpair 3 --maxspk 1166 --maxword 4 --mode diffspk_all

# samespk_easy mode
# python3 libriphrase.py  \
# --libripath /home/hkshin/server_hdd/Database/LibriSpeech_clean_wav/  \
# --newpath /home/hkshin/server_hdd/Database/LibriPhrase_samespk_easy/  \
# --wordalign ./data/librispeech_other_train_500h_all_utt.csv  \
# --output ./data/libriphrase_samespk_easy.csv  \
# --numpair 3 --maxspk 1166 --maxword 4 --mode samespk_easy

# diffspk_easy mode
# python3 libriphrase.py  \
# --libripath /home/hkshin/server_hdd/Database/LibriSpeech_clean_wav/  \
# --newpath /home/hkshin/server_hdd/Database/LibriPhrase_diffspk_easy/  \
# --wordalign ./data/librispeech_other_train_500h_all_utt.csv  \
# --output ./data/libriphrase_diffspk_easy.csv  \
# --numpair 3 --maxspk 1166 --maxword 4 --mode diffspk_easy

# diffspk_hard mode
# python3 libriphrase.py  \
# --libripath /home/hkshin/server_hdd/Database/LibriSpeech_clean_wav/  \
# --newpath /home/hkshin/server_hdd/Database/LibriPhrase_diffspk_hard/  \
# --wordalign ./data/librispeech_other_train_500h_all_utt.csv  \
# --output ./data/libriphrase_diffspk_hard.csv  \
# --numpair 3 --maxspk 1166 --maxword 4 --mode diffspk_hard

