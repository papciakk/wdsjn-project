# coding=utf-8
import pickle
import re
from operator import itemgetter

import morfeusz2

from basic_forms.data_utils import read_words

morfeusz = morfeusz2.Morfeusz(dict_name="polimorf")


def text_before_colon(word):
    return word.partition(":")[0]


def generate(word):
    results = morfeusz.generate(word)
    results = [text_before_colon(r[0]) for r in results]
    return results


def analyze(word):
    results = morfeusz.analyse(word)
    return text_before_colon(results[0][2][1])


def strip_word(word):
    return re.sub(u"[^a-zA-ZĘÓĄŚŁŻŹĆŃęóąśłżźćń]", " ", word).strip()


dict = {}
dict_id = 0

text_word_ids = []

for word in read_words("../data/plwiki_raw.txt", buff_size=1024 * 1024):
    w = strip_word(word)
    if len(w) > 0:
        word_bf = analyze(w)

        if word_bf not in dict:
            dict[word_bf] = dict_id
            dict_id += 1

        text_word_ids.append(dict[word_bf])

rev_dict = [word for word, _ in sorted(dict.items(), key=itemgetter(1))]

result = {"text": text_word_ids, "dict": dict, "rev_dict": rev_dict}

with open("result.pickle", "wb") as f:
    pickle.dump(result, f)