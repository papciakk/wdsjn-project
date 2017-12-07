import pickle
from sys import argv

from collections import defaultdict

import plp
from corpus_loader import load

if len(argv) != 3:
    print("usage:", argv[0], "<in filename>", "<out filename>")
    exit(1)

p = plp.PLP()

unrecognized_cnt = 0


def get_basic_form_if_available(word):
    global unrecognized_cnt
    word_ids = p.orec(word)
    if len(word_ids) != 0:
        return p.bform(word_ids[0])

    unrecognized_cnt += 1
    return None


def save(filename, data):
    with open("work/" + filename, "wb") as file:
        pickle.dump(data, file)


print("loading data from " + argv[1])
corpus = load("data/" + argv[1])
print("converting")

text = []
dict = {}
counts = defaultdict(int)

for i, word in enumerate(corpus):
    bf = get_basic_form_if_available(word)

    if bf is not None:
        if bf in dict:
            word_id = dict[bf]
        else:
            word_id = len(dict)
            dict[bf] = word_id

        counts[bf] += 1

        text.append(word_id)

    else:
        print("unrecognized: " + word)

    if i % 1000 == 0:
        print("{:.2f} %".format(i / len(corpus) * 100))

print("saving text to:", argv[2]+"_text.p")
save(argv[2]+"_text.p", text)

print("saving dict to:", argv[2]+"_dict.p")
save(argv[2]+"_dict.p", dict)

print("saving counts to:", argv[2]+"_counts.p")
save(argv[2]+"_dict.p", counts)

reverse_dict = [None]*len(dict)
for word, id in dict.items():
    reverse_dict[id] = word

print("saving reverse dict to:", argv[2]+"_rdict.p")
save(argv[2]+"_rdict.p", reverse_dict)
