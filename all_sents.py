import pandas as pd 
import re

stop_words = [',', '.', '-', '_', "'", '"', '،']

data_df = pd.read_csv('dataset_3m.csv')
subword_df = pd.read_csv('ambg-subword.csv')
word_df = pd.read_csv('ambg-words.csv')

def modify_sent(wenglish, wfarsi):
    for word in subword_df['persian_word'].unique():
        for idx, wf in enumerate(wfarsi):
            if word not in wf:
                continue 
            
            wes = subword_df[subword_df['persian_word'] == word]
            possible_list = []
            for _, we in wes.iterrows():
                isin = True 
                for part in we['english_word'].split('|'):
                    if part not in wenglish:
                        isin = False 
                        break
                if isin:
                    possible_list.append(we)
            if len(possible_list) == 1:
                if '|' in we['english_word']:
                    print(possible_list, ' '.join(wenglish), ' '.join(wfarsi), sep='-------------\n')
                wpossible = possible_list[0]
                print(' '.join(wenglish), wpossible['english_word'], wpossible['persian_word_eraab'], word)
                wfarsi[idx] = wf.replace(word, wpossible['persian_word_eraab'])
                print(wfarsi[idx], wf.replace(word, wpossible['persian_word_eraab']))
            
            # word replacement
            for sw in stop_words:
                wf = wf.replace(sw, '')
            if word not in wf.split('\u200c'):
                continue 
            
            wes = word_df[word_df['persian_word'] == word]
            possible_list = []
            for _, we in wes.iterrows():
                isin = True 
                for part in we['english_word'].split('|'):
                    if part not in wenglish:
                        isin = False 
                        break
                if isin:
                    possible_list.append(we)
            if len(possible_list) == 1:
                if '|' in we['english_word']:
                    print(possible_list, ' '.join(wenglish), ' '.join(wfarsi), sep='-------------\n')
                wpossible = possible_list[0]
                print(' '.join(wenglish), wpossible['english_word'], wpossible['persian_word_eraab'], word)
                wfarsi[idx] = '\u200c'.join(wpossible['persian_word_eraab'] if wpossible['persian_word'] == w else w for w in wf.split('\u200c'))
                print(wfarsi[idx], wpossible['persian_word_eraab'])

with open('all_sents.txt', 'w') as f:
    for _, record in data_df.iterrows():
        wenglish = record['source'].strip().split()
        wfarsi = record['target'].strip().split()
        modify_sent(wenglish, wfarsi)
        if wfarsi != record['target'].strip().split(): f.write(f"{record['idx']}|{' '.join(wfarsi).strip()}\n")
    