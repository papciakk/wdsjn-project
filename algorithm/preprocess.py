import collections
import pickle
import pprint

import numpy as np

from algorithm.timer import Timer

stoplist_percent = 0.3


def run():
    with Timer("load data"):
        text, text_size = load_text()
        rdict = load_rdict()

    with Timer("prepare word ranking"):
        counter = collections.Counter(text)
        counter_most_common = counter.most_common(1000)

    with Timer("prepare stoplist"):
        stoplist = prepare_stoplist(counter_most_common, text_size)
        # save_data(stoplist, "stoplist")

    with Timer("prepare hapax legomena"):
        hapax_legomena = prepare_hapax_legomena(counter)
        # save_data(hapax_legomena, "hapax_legomena")

    with Timer("find too short words"):
        too_short_words = find_too_short_words(rdict)

    # print_stoplist(rdict, stoplist)
    # print("hapax legomena count:", len(hapax_legomena))

    del counter
    del counter_most_common

    word_ids_to_remove = []
    word_ids_to_remove.extend(stoplist)
    word_ids_to_remove.extend(hapax_legomena)
    word_ids_to_remove.extend(too_short_words)
    word_ids_to_remove = set(word_ids_to_remove)

    with Timer("filter text"):
        filtered_text = filter_text(text, word_ids_to_remove)
        save_data(filtered_text, "filtered_text")


def find_too_short_words(rdict):
    return [word_id for word_id, word in enumerate(rdict) if len(word) < 3]


def filter_text(text, word_ids_to_remove):
    filtered_text = np.array(
        [word_id for word_id in text
         if word_id not in word_ids_to_remove],
        dtype=np.int32)
    del text
    return filtered_text


def print_stoplist(rdict, stoplist):
    pprint.pprint([rdict[w] for w in stoplist])
    print("stoplist count:", len(stoplist))


def save_data(data, name):
    with open(name + ".pickle", "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def prepare_hapax_legomena(counter):
    hapax_legomena = []
    for word_id, count in counter.items():
        if count < 2:
            hapax_legomena.append(word_id)
    return hapax_legomena


def save_stoplist(stop_words):
    with open("stoplist.pickle", "wb") as f:
        pickle.dump(stop_words, f)


def prepare_stoplist(counter_most_common, text_size):
    percent = 0.0
    stop_words = []
    for word_id, count in counter_most_common:
        percent += float(count) / text_size

        stop_words.append(word_id)

        if percent >= stoplist_percent:
            break

    return stop_words


def load_rdict():
    with open("rdict.pickle", "rb") as f:
        rdict = pickle.load(f)
    return rdict


def load_text():
    with open("text.pickle", "rb") as f:
        text = pickle.load(f)
    text_size = len(text)
    return text, text_size


run()
