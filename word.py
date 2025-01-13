import pandas as pd 

stop_words = [',', '.', '-', '_', "'", '"', '،']

data_df = pd.read_csv('dataset_3m.csv')
word_df = pd.read_csv('ambg-words.csv')

def modify_sent(wenglish, wfarsi):
    for word in word_df['persian_word'].unique():
        for idx, wf in enumerate(wfarsi):
            for sw in stop_words:
                wf = wf.replace(sw, '')
            if word != wf:
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
                wfarsi[idx] = wpossible['persian_word_eraab']
                print(wfarsi[idx], wpossible['persian_word_eraab'])
                

with open('word_sents.txt', 'w') as f:
    for _, record in data_df.iterrows():
        wenglish = record['source'].strip().split()
        wfarsi = record['target'].strip().split()
        modify_sent(wenglish, wfarsi)
        if wfarsi != record['target'].strip().split(): f.write(' '.join(wfarsi).strip() + '\n')
    