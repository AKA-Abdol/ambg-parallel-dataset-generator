file_path = "../all_sents.txt"


def read_sentences(file_path, select_index=0, sep='|'):
    sentences = []
    with open(file_path) as f:
        for line in f:
            sentences.append(line.split(sep)[select_index])
    return sentences


sentences = read_sentences(file_path=file_path, select_index=1)

diacritics = ['ِ', 'َ', 'ُ', 'ْ', 'ٌ', 'ٍ', 'ً', 'ّ']


def get_diacritics_index(word):
    indexes = []
    for idx in range(len(word)):
        if word[idx] in diacritics:
            indexes.append(idx)
    return indexes


def remove_diacritics(text):
    for diac in diacritics:
        text = text.replace(diac, '')
    return text


def augment_by_word_sub_diacritics(sentence, max_word_aug_count=3):
    without_diac_words = remove_diacritics(sentence)
    words_without_diacritics = without_diac_words.split()
    sentences = [sentence, without_diac_words]
    words = sentence.split()
    diac_indexes_list = [get_diacritics_index(word) for word in words]
    diac_count = 0
    for diac_indexes in diac_indexes_list:
        diac_count += len(diac_indexes)
    can_augment_more = diac_count > 1
    if can_augment_more:
        for idx, word in enumerate(words):
            diac_indexes = diac_indexes_list[idx]
            # print(diac_indexes)
            if not len(diac_indexes):
                continue
            for j, diac_idx in enumerate(diac_indexes):
                if j >= max_word_aug_count:
                    break
                aug_word = remove_diacritics(
                    word[:diac_idx]) + word[diac_idx] + remove_diacritics(word[diac_idx + 1:])
                sentences.append(
                    (' '.join(words_without_diacritics[:idx]) + f' {aug_word} ' + ' '.join(words_without_diacritics[idx+1:])).strip())
    return sentences


# print(remove_diacritics('سالِمتَر از اُرومیه نیسْت قطعاً'))
# print(get_diacritics_index('کِتابَمُن'))
with open('dataset.csv', 'w', encoding='utf-8') as f:
    for idx, sentence in enumerate(sentences):
        sentence = sentence.strip()
        augmented_sentences = augment_by_word_sub_diacritics(
            sentence, max_word_aug_count=5)
        for aug_sent in augmented_sentences:
            f.write(aug_sent + '|' + sentence + '\n')
        if idx % 1000 == 0:
            print(f'{(idx * 100/len(sentences)):.2f}% progress')
print('finished')
