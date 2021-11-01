from collections import Counter, defaultdict
from tqdm import tqdm
import os
from os.path import dirname, splitext, basename
import numpy as np
import pandas as pd
from pydub import AudioSegment 
import itertools




def load_csv(filename):
  df = pd.read_csv(filename, na_filter=False)
  return df


def make_dic(df_word):
  dic = {}
  audio_lst = list(set(list(set(df_word['anchor'])) + list(set(df_word['comparison']))))
  for i in tqdm(range(0, len(audio_lst))):
    dic[audio_lst[i]] = 0
  return dic


def save_wav(df, rootpath, rootpath_new, word_class):
  count_dic = make_dic(df)
  result = []
  for idx, row in tqdm(df.iterrows()):
    audio = AudioSegment.from_wav(rootpath + row['anchor'])
    audio = audio[row['anchor_start'] * 1000.0 : row['anchor_end'] * 1000.0]
    new_filename = dirname(row['anchor']) + os.sep + splitext(basename(row['anchor']))[0] + '_' + word_class + '_' + str(count_dic[row['anchor']]) + '.wav'

    if os.path.isdir(dirname(rootpath_new + new_filename)) == False:
      os.makedirs(dirname(rootpath_new + new_filename))
    audio.export(rootpath_new + new_filename, format='wav')
    count_dic[row['anchor']] += 1


    audio2 = AudioSegment.from_wav(rootpath + row['comparison'])
    audio2 = audio2[row['comparison_start'] * 1000.0 : row['comparison_end'] * 1000.0]
    new_filename2 = dirname(row['comparison']) + os.sep + splitext(basename(row['comparison']))[0] + '_' + word_class + '_' + str(count_dic[row['comparison']]) + '.wav'

    if os.path.isdir(dirname(rootpath_new + new_filename2)) == False:
      os.makedirs(dirname(rootpath_new + new_filename2))
    audio2.export(rootpath_new + new_filename2, format='wav')
    count_dic[row['comparison']] += 1


    dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_dur': '', \
           'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_dur': '', \
           'type': '', 'target': '', 'class': ''}

    dic['anchor'] = new_filename
    dic['anchor_spk'] = row['anchor_spk']
    dic['anchor_text'] = row['anchor_text']
    dic['anchor_dur'] = row['anchor_dur']
    dic['comparison'] = new_filename2
    dic['comparison_spk'] = row['comparison_spk']
    dic['comparison_text'] = row['comparison_text']
    dic['comparison_dur'] = row['comparison_dur']
    dic['type'] = row['type']
    dic['target'] = row['target']
    dic['class'] = row['class']
    result.append(dic)


  df_wav = pd.DataFrame(result)
  return df_wav



def levenshtein(s1, s2, limit_dist=1, debug=False):
  '''
  Do not consider distance limit_dist in 'insertion', 'deletion'
  '''
  s1 = ''.join(s1)
  s2 = ''.join(s2)
 
  if len(s1) < len(s2):
    return levenshtein(s2, s1, limit_dist, debug)
  if len(s2) == 0:
    return len(s1)
  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1 
      deletions = current_row[j] + 1
      substitutions = previous_row[j] + (c1 != c2)
      if insertions <= limit_dist and deletions > limit_dist:
        current_row.append(min(deletions, substitutions))
      elif insertions > limit_dist and deletions <= limit_dist:
        current_row.append(min(insertions, substitutions))
      elif insertions <= limit_dist and deletions <= limit_dist:
        current_row.append(substitutions)
      else:
        current_row.append(min(insertions, deletions, substitutions))
    if debug:
      print(current_row[1:])
    previous_row = current_row
  return previous_row[-1]


def make_k_spk_dict(df, k):

  # extract speaker list by counting spk's words (k speakers)
  spk_lst = [dirname(af).split('/')[-2] for af in df['audio_filename']]
  print('len(Counter(spk_lst)) = ', len(Counter(spk_lst)))
  spk_dic = dict(Counter(spk_lst).most_common(k))
  print('len(spk_dic) = ', len(spk_dic))

  return spk_dic


def extract_anchor(df, spk_dic, num_anchor, num_pos):

  # extract anchor by counting words in each speaker (num_anchor + num_pos samples can be selected as anchor)

  ## make word count dictionary for each speaker (in 500 speakers)
  word_cnt_dic = defaultdict(list)
  for idx, row in tqdm(df.iterrows()):
    spk_id = dirname(row['audio_filename']).split('/')[-2]
    if spk_id in list(spk_dic.keys()):
      word_cnt_dic[spk_id].append(row['text'])
  print('len(word_cnt_dic) = ', len(word_cnt_dic))

  ## extract over (num_anchor + num_pos) words for selecting anchor  
  anchor_word_dic = defaultdict(list)
  for key, value in tqdm(word_cnt_dic.items()):
    cnt_word = Counter(value)
    for word in cnt_word:
      if cnt_word[word] >= num_anchor + num_pos:
        if '  ' not in word:
          lst = [word for k, v in word_cnt_dic.items() if k != key and word in v] # different speaker and same text
        else:
          print('word = ', word)
        if len(lst) >= num_pos:
          anchor_word_dic[key].append(word)
  print('len(anchor_word_dic.keys()) = ', len(anchor_word_dic.keys()))

  ## count # of episodes
  anchor_lst = []
  for key, value in tqdm(anchor_word_dic.items()):
     anchor_lst.extend(value)
  print('len(anchor_lst) (# of episode) = ', len(anchor_lst))

  return anchor_word_dic, anchor_lst
      

def extract_total_word(df, word_lst, g2p):
  
  # extract total word in specific speakers
  total_word_dic = defaultdict(list)
  for i in tqdm(range(len(word_lst))):
    total_word_dic[word_lst[i]].extend([phn.replace('0', '').replace('1', '').replace('2', '') for phn in g2p(word_lst[i])])
 
  return total_word_dic 


def make_hard_negative(anchor_word_dic, total_word_dic, num_neg, word_class):
  # easy_negative: same or different speaker, random negative except hard negative
  # hard_negative: same or different speaker, hard negative using levenshtien distance

  max_dist = int(5 * (word_class + 2)) # to reduce computation in levenshtein
  print('max_dist = ', max_dist)

  hard_neg_dic = defaultdict(list)

  anchor_values = list(itertools.chain(*list(anchor_word_dic.values())))
  print('len(anchor_values) = ', len(anchor_values))
  anchor_values = list(set(anchor_values))
  print('len(anchor_values) = ', len(anchor_values))
  for value in tqdm(anchor_values):
    ele_dic = {}
    for k_ele in list(total_word_dic.keys()):
      ED = levenshtein(total_word_dic[value], total_word_dic[k_ele], limit_dist=1)
      if ED > 0 and ED <= max_dist:
        ele_dic[k_ele] = int(ED)
 
    temp_dic = sorted(ele_dic.items(), key=lambda item: item[1])
    hard_neg_dic[value].extend([temp_dic[i] for i in range(0, num_neg)])
  return hard_neg_dic


def make_negative(hard_neg_dic, df_dic_key, df_result_pos, num_neg, mode, word_class):
  # different speaker, easy negative
  # different speaker, hard negative
  # same speaker, easy(random) negative
  result = []
  anchor_cnt = {(row['anchor_spk'], row['anchor_text'], row['anchor'], row['anchor_start'], row['anchor_end']): 0 for idx, row in df_result_pos.iterrows()}


  print('len(df_result_pos) = ', len(df_result_pos))
  for idx, row in tqdm(df_result_pos.iterrows()):
    k_tuple = (row['anchor_spk'], row['anchor_text'], row['anchor'], row['anchor_start'], row['anchor_end'])
    if mode in ['diffspk_hard', 'diffspk_all']:
      hard_neg_text = hard_neg_dic[row['anchor_text']]

    if anchor_cnt[k_tuple] == 1:
      continue

    anchor_cnt[k_tuple] += 1

    # get rows    
    easy_neg_rows = []
    hard_neg_rows = []
    same_neg_rows = [] 

    ## diffspk easy negative
    if mode in ['diffspk_easy', 'diffspk_all']:
      total_tuple = [(dk[0], dk[1]) for dk in list(set(df_dic_key.keys())) if dk[1]!=row['anchor_text']]
      other_tuple_idx = np.random.choice(range(0, len(total_tuple)), num_neg, replace=False)
      other_tuple = [total_tuple[i] for i in other_tuple_idx]

      for e_tuple in other_tuple:
        other_rows = df_dic_key[e_tuple]
        easy_neg_rows.append(other_rows[int(np.random.choice(range(0, len(other_rows)), 1, replace=False))])
      if len(easy_neg_rows) != num_neg:
        print('len(easy_neg_rows) = ', len(easy_neg_rows))
        raise Exception('Easy neg rows is not same with num_neg!')

    ## diffspk hard negative
    if mode in ['diffspk_hard', 'diffspk_all']:
      for hnt, hnt_cnt in hard_neg_text:
        total_key = [dk[0] for dk in list(set(df_dic_key.keys())) if dk[1]==hnt]
        other_key_diff = total_key[int(np.random.choice(range(0, len(total_key)), 1, replace=False))]

        h_tuple = (other_key_diff, hnt)
        other_rows = df_dic_key[h_tuple]
        hard_neg_rows.append(other_rows[int(np.random.choice(range(0, len(other_rows)), 1, replace=False))])
      if len(hard_neg_rows) != num_neg:
        print('len(hard_neg_rows) = ', len(hard_neg_rows))
        raise Exception('Hard neg rows is not same with num_neg!')


    ## same spk negative
    if mode == 'samespk_easy': 
      total_tuple = [(dk[0], dk[1]) for dk in list(set(df_dic_key.keys())) if dk[1]!=row['anchor_text'] and dk[0]==row['anchor_spk']]
      other_value_same_idx = np.random.choice(range(0, len(total_tuple)), num_neg, replace=False)
      other_value_same = [total_tuple[i] for i in other_value_same_idx]

      for s_tuple in other_value_same:
        other_rows = df_dic_key[s_tuple]
        same_neg_rows.append(other_rows[int(np.random.choice(range(0, len(other_rows)), 1, replace=False))])
      if len(same_neg_rows) != num_neg:
        print('len(same_neg_rows) = ', len(same_neg_rows))
        raise Exception('Same spk neg rows is not same with num_neg!')


    # save dataframe
    for i in range(0, num_neg):
      ## easy negative 
      if mode in ['diffspk_easy', 'diffspk_all']:
        dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_start': '', 'anchor_end': '', 'anchor_dur': '', \
               'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_start': '', 'comparison_end': '', 'comparison_dur': '', \
               'type': '', 'target': '', 'class': ''} 
        dic['anchor'] = row['anchor']
        dic['anchor_spk'] = row['anchor_spk']
        dic['anchor_text'] = row['anchor_text']
        dic['anchor_start'] = row['anchor_start']
        dic['anchor_end'] = row['anchor_end']
        dic['anchor_dur'] = row['anchor_dur']
        dic['comparison'] = easy_neg_rows[i]['audio_filename']
        dic['comparison_spk'] = easy_neg_rows[i]['speaker']
        dic['comparison_text'] = easy_neg_rows[i]['text']
        dic['comparison_start'] = easy_neg_rows[i]['start']
        dic['comparison_end'] = easy_neg_rows[i]['end']
        dic['comparison_dur'] = easy_neg_rows[i]['dur']  
        dic['type'] = 'diffspk_easyneg'
        dic['target'] = 0
        dic['class'] = word_class
        result.append(dic)  
     
      ## hard negative
      if mode in ['diffspk_hard', 'diffspk_all']:
        dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_start': '', 'anchor_end': '', 'anchor_dur': '', \
               'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_start': '', 'comparison_end': '', 'comparison_dur': '', \
               'type': '', 'target': '', 'class': ''} 
        dic['anchor'] = row['anchor']
        dic['anchor_spk'] = row['anchor_spk']
        dic['anchor_text'] = row['anchor_text']
        dic['anchor_start'] = row['anchor_start']
        dic['anchor_end'] = row['anchor_end']
        dic['anchor_dur'] = row['anchor_dur']
        dic['comparison'] = hard_neg_rows[i]['audio_filename']
        dic['comparison_spk'] = hard_neg_rows[i]['speaker']
        dic['comparison_text'] = hard_neg_rows[i]['text']
        dic['comparison_start'] = hard_neg_rows[i]['start']
        dic['comparison_end'] = hard_neg_rows[i]['end']
        dic['comparison_dur'] = hard_neg_rows[i]['dur']  
        dic['type'] = 'diffspk_hardneg'
        dic['target'] = 0
        dic['class'] = word_class
        result.append(dic)  

      ## same spk negative
      if mode == 'samespk_easy':
        dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_start': '', 'anchor_end': '', 'anchor_dur': '', \
               'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_start': '', 'comparison_end': '', 'comparison_dur': '', \
               'type': '', 'target': '', 'class': ''} 
        dic['anchor'] = row['anchor']
        dic['anchor_spk'] = row['anchor_spk']
        dic['anchor_text'] = row['anchor_text']
        dic['anchor_start'] = row['anchor_start']
        dic['anchor_end'] = row['anchor_end']
        dic['anchor_dur'] = row['anchor_dur']
        dic['comparison'] = same_neg_rows[i]['audio_filename']
        dic['comparison_spk'] = same_neg_rows[i]['speaker']
        dic['comparison_text'] = same_neg_rows[i]['text']
        dic['comparison_start'] = same_neg_rows[i]['start']
        dic['comparison_end'] = same_neg_rows[i]['end']
        dic['comparison_dur'] = same_neg_rows[i]['dur']  
        dic['type'] = 'samespk_easyneg'
        dic['target'] = 0
        dic['class'] = word_class
        result.append(dic)  
 
  df_result = pd.DataFrame(result)
  return df_result
          

def make_positive(anchor_word_dic, df_dic_key, num_anchor, num_pos, mode, word_class):
  # same speaker, positive
  # different speaker, positive
  result = []
  for key, value in tqdm(anchor_word_dic.items()):
    for v in value:
      if len(v.split(' ')) == word_class:
        k_tuple = (key, v)
        rows = df_dic_key[k_tuple]
        a_p_rows_idx = np.random.choice(range(0, len(rows)), num_anchor + num_pos, replace=False)
        anchor_rows = [rows[a_p_rows_idx[a_idx]] for a_idx in range(0, num_anchor)] # anchor 
        postive_rows = [rows[a_p_rows_idx[p_idx]] for p_idx in range(num_anchor, num_anchor + num_pos)] # same speaker positive

        total_key = [(dk[0], dk[1]) for dk in df_dic_key.keys() if dk[1]==v and dk[0]!=key] # differnt speaker positive
        other_diff = np.random.choice(range(0, len(total_key)), num_pos, replace=False)
        other_diff_rows = [total_key[od] for od in other_diff]
        diffspk_rows_lst = []
        for d_tuple in other_diff_rows:
          other_rows = df_dic_key[d_tuple]
          diffspk_rows_lst.append(other_rows[int(np.random.choice(range(0, len(other_rows)), 1, replace=False))])

        if len(diffspk_rows_lst) != num_pos:
          print('len(diffspk_rows_lst) = ', len(diffspk_rows_lst))
          raise Exception('Diffspk positive sample is not same with num_pos')

        for a_row in anchor_rows:
          if mode == 'samespk_easy':
            for s_row in postive_rows:
              dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_start': '', 'anchor_end': '', 'anchor_dur': '', \
                     'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_start': '', 'comparison_end': '', 'comparison_dur': '', \
                     'type': '', 'target': '', 'class': ''}
              dic['anchor'] = a_row['audio_filename']
              if a_row['speaker'] != key:
                raise Exception("Anchor speaker is different")
              dic['anchor_spk'] = a_row['speaker']
              dic['anchor_text'] = a_row['text']
              dic['anchor_start'] = a_row['start']
              dic['anchor_end'] = a_row['end']
              dic['anchor_dur'] = a_row['dur']
              dic['comparison'] = s_row['audio_filename']
              dic['comparison_spk'] = s_row['speaker']
              dic['comparison_text'] = s_row['text']
              dic['comparison_start'] = s_row['start']
              dic['comparison_end'] = s_row['end']
              dic['comparison_dur'] = s_row['dur']
              dic['type'] = 'samespk_positive'
              dic['target'] = 1
              dic['class'] = word_class
              result.append(dic)  

          elif mode in ['diffspk_easy', 'diffspk_hard', 'diffspk_all']:           
            for d_row in diffspk_rows_lst:
              dic = {'anchor': '', 'anchor_spk': '', 'anchor_text': '', 'anchor_start': '', 'anchor_end': '', 'anchor_dur': '', \
                     'comparison': '', 'comparison_spk': '', 'comparison_text': '', 'comparison_start': '', 'comparison_end': '', 'comparison_dur': '', \
                     'type': '', 'target': '', 'class': ''}
              dic['anchor'] = a_row['audio_filename']
              dic['anchor_spk'] = a_row['speaker']
              dic['anchor_text'] = a_row['text']
              dic['anchor_start'] = a_row['start']
              dic['anchor_end'] = a_row['end']
              dic['anchor_dur'] = a_row['dur']
              dic['comparison'] = d_row['audio_filename']
              dic['comparison_spk'] = d_row['speaker']
              dic['comparison_text'] = d_row['text']
              dic['comparison_start'] = d_row['start']
              dic['comparison_end'] = d_row['end']
              dic['comparison_dur'] = d_row['dur']
              dic['type'] = 'diffspk_positive'
              dic['target'] = 1
              dic['class'] = word_class
              result.append(dic)

  df_result = pd.DataFrame(result)
  return df_result


def extract_df_word_class(df, word_class):
  result = []
  for idx, row in tqdm(df.iterrows()): 
    if row['class'] == 'word_' + str(word_class):
      dic = {'audio_filename': '', 'start': '', 'end': '', 'text': '', 'dur': '', 'class': '', 'speaker': ''}
      dic['audio_filename'] = row['audio_filename']
      dic['start'] = row['start']
      dic['end'] = row['end']
      dic['text'] = row['text']
      dic['dur'] = row['dur']
      dic['class'] = row['class']
      dic['speaker'] = dirname(row['audio_filename']).split('/')[-2]
      result.append(dic)
  df_word_class = pd.DataFrame(result)
  return df_word_class
 

def extract_short_phrase_from_csv(csv_file):
  df = pd.read_csv(csv_file, na_filter=False)
  file_lst = list(set(df['audio_filename']))
  file_dic = defaultdict(list)
  for idx, row in tqdm(df.iterrows()):
    dur = float(row['end']) - float(row['start'])
    file_dic[row['audio_filename']].append([row['start'], row['end'], row['text'], dur])

  result_lst = []

  ### extract word1
  for k, v in tqdm(file_dic.items()):
    for i in range(len(v)): 
      if v[i][2] in ['<unk>', '']:
        continue
      elif v[i][3] >= 0.5 and v[i][3] <= 2:
        word_dic = {'audio_filename': k, 'start': v[i][0], 'end': v[i][1], 'text': v[i][2], 'dur': v[i][3], 'class': 'word_1', 'speaker': dirname(k).split('/')[-2]}
        result_lst.append(word_dic)
  print('word 1 len(result_lst) = ', len(result_lst))

  ### extract word2
  for k, v in tqdm(file_dic.items()):
    for i in range(len(v)-1):
      if v[i][2] in ['<unk>', '']:
        continue
      elif v[i+1][2] in ['<unk>', '']:
        continue
      elif float(v[i][3]) + float(v[i+1][3]) >= 0.5 and float(v[i][3]) + float(v[i+1][3]) <= 2:
        word_dic = {'audio_filename': k, 'start': v[i][0], 'end': v[i+1][1], 'text': ' '.join([v[i][2], v[i+1][2]]), 'dur': float(v[i][3]) + float(v[i+1][3]), 'class': 'word_2', 'speaker': dirname(k).split('/')[-2]}
        result_lst.append(word_dic)
  print('word 2 len(result_lst) = ', len(result_lst))

  ### extract word3
  for k, v in tqdm(file_dic.items()):
    for i in range(len(v)-2):
      if v[i][2] in ['<unk>', '']:
        continue
      elif v[i+1][2] in ['<unk>', '']:
        continue
      elif v[i+2][2] in ['<unk>', '']:
        continue
      elif float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]) >= 0.5 and float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]) <= 2:
        word_dic = {'audio_filename': k, 'start': v[i][0], 'end': v[i+2][1], 'text': ' '.join([v[i][2], v[i+1][2], v[i+2][2]]), 'dur': float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]), 'class': 'word_3', 'speaker': dirname(k).split('/')[-2]}
        result_lst.append(word_dic)
  print('word 3 len(result_lst) = ', len(result_lst))

  ### extract word4
  for k, v in tqdm(file_dic.items()):
    for i in range(len(v)-3):
      if v[i][2] in ['<unk>', '']:
        continue
      elif v[i+1][2] in ['<unk>', '']:
        continue
      elif v[i+2][2] in ['<unk>', '']:
        continue
      elif v[i+3][2] in ['<unk>', '']:
        continue
      elif float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]) + float(v[i+3][3]) >= 0.5 and float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]) + float(v[i+3][3]) <= 2:
        word_dic = {'audio_filename': k, 'start': v[i][0], 'end': v[i+3][1], 'text': ' '.join([v[i][2], v[i+1][2], v[i+2][2], v[i+3][2]]), 'dur': float(v[i][3]) + float(v[i+1][3]) + float(v[i+2][3]) + float(v[i+3][3]), 'class': 'word_4', 'speaker': dirname(k).split('/')[-2]}
        result_lst.append(word_dic)
  print('word 4 len(result_lst) = ', len(result_lst))

  df_short_phrase = pd.DataFrame(result_lst)

  return df_short_phrase


