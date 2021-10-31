import argparse
from collections import defaultdict
from os.path import splitext, dirname
from g2p_en import G2p
import pandas as pd
from utils import *




def get_parser():
  parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--libripath', type=str, default='/home/hkshin/server_hdd/Database/LibriSpeech_clean_wav/', help='root path of LibriSpeech (wav format)')
  parser.add_argument('--newpath', type=str, default='/home/hkshin/server_hdd/Database/LibriSpeech_testset_short_phrase/', help='new root path')
  parser.add_argument('--wordalign', type=str, default='./data/librispeech_other_train_500h_all_utt.csv', help='word alignment (csv format)')
  parser.add_argument('--output', type=str, default='./data/testset_librispeech_other_train_500h_short_phrase.csv', help='output filename (csv format)')
  parser.add_argument('--numpair', type=int, default=3)
  parser.add_argument('--maxspk', type=int, default=1166, help='the maximum number of speakers (default: 1166)')
  parser.add_argument('--maxword', type=int, default=4, help='the maximum number of words (default: 4)')
  parser.add_argument('--mode', type=str, default='diffspk_all', choices=['samespk_easy', 'diffspk_easy', 'diffspk_hard', 'diffspk_all'])
  return parser


def main(args):

  rootpath = args.libripath
  rootpath_new = args.newpath
  word_alignment = args.wordalign
  output_filename = args.output
  
  # set parameters
  spk_k = args.maxspk
  max_num_words = args.maxword
  num_anchor = args.numpair
  num_pos = args.numpair
  num_neg = args.numpair
  mode = args.mode

  df = extract_short_phrase_from_csv(word_alignment)
  print('len(df) = ', len(df))


  spk_dic = make_k_spk_dict(df, spk_k)
  g2p = G2p()

  # extract 'anchor candidates'
  anchor_word_dic, anchor_lst = extract_anchor(df, spk_dic, num_anchor, num_pos)

  for i in range(1, max_num_words + 1):
    # confirm word_class
    print('word class = ', i)
     
    # extract 'df' and 'word_lst' which are only included word_class
    df_word_class = extract_df_word_class(df, i)
    word = [row['text'] for idx, row in df_word_class.iterrows()]
    word_lst = list(set(word))

    # extract 'df_dic_key'
    print('-----start making df_dic_key-------')
    df_dic_key = defaultdict(list)
    for idx, row in df_word_class.iterrows():
      df_dic_key[(dirname(row['audio_filename']).split('/')[-2], row['text'])].append(row)       
    
    # make positive 
    print('-----start making positive-------')
    df_result_pos = make_positive(anchor_word_dic, df_dic_key, num_anchor, num_pos, mode, word_class=i)
    
    # make negative
    print('-----start making negative-------')
    total_word_dic = extract_total_word(df, word_lst, g2p) 
    if mode in ['diffspk_hard', 'diffspk_all']:
      hard_neg_dic = make_hard_negative(anchor_word_dic, total_word_dic, num_neg, word_class=i)
    else:
      hard_neg_dic = None
    df_result_neg = make_negative(hard_neg_dic, df_dic_key, df_result_pos, num_neg, mode, word_class=i)

    print('len(df_result_pos) = ', len(df_result_pos))
    print('len(df_result_neg) = ', len(df_result_neg))

    # merge and save 'df_result_pos' and 'df_result_neg'
    total_df = pd.concat([df_result_pos, df_result_neg], ignore_index=True)
    total_df = total_df.sort_values(by=['anchor_spk', 'anchor_text', 'target', 'type', 'comparison_spk'], ascending=[True, True, True, True, True])
    total_df = total_df.reset_index(drop=True)
    print('-----start exporting wav files-------')
    total_df = save_wav(total_df, rootpath, rootpath_new)
    total_df = total_df.sort_values(by=['anchor_spk', 'anchor_text', 'target', 'type', 'comparison_spk'], ascending=[True, True, True, True, True])
    total_df = total_df.reset_index(drop=True)
    print('-----save csv file-------')
    total_df.to_csv(splitext(output_filename)[0] + '_' + str(i) + 'word' + splitext(output_filename)[1], index=False)
    print('finish {} word class'.format(i))    


if __name__ == '__main__':
  
  args = get_parser().parse_args()
  main(args)




