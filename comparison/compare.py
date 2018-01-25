import csv
import os

import numpy as np

stimuli_words = ["liść", "kwiat", "łodyga", "roślina"]


def compare(stimuli, current_result_dir, comparator):
    with open("{}/{}.txt".format(current_result_dir, stimuli), "r", encoding="utf8") as result_f:
        with open("../data/stimuli/{}.csv".format(stimuli), "r", encoding="utf8") as reference_f:
            reference_data = prepare_reference_data(reference_f)
            result_data = prepare_result_data(result_f)

            length = comparator(reference_data, result_data)

    return length


def basic_comparator(reference_data, result_data, compare_count=25):
    vector = {}
    for reference_data_item in reference_data:
        words_ref = reference_data_item[0]
        val_ref = reference_data_item[1]

        for result_dat_item in result_data[:compare_count]:
            word_res = result_dat_item[0]
            val_res = result_dat_item[1]

            if word_res in words_ref:
                vector[word_res] = val_res - val_ref
                break
            else:
                vector[word_res] = val_res

    length = np.sqrt(np.sum(v ** 2 for v in vector.values()))
    return length


def position_comparator(reference_data, result_data, compare_count=25):
    vector = {}

    for position_res, result_dat_item in enumerate(result_data[:compare_count]):
        word_res = result_dat_item[0]

        for position_ref, reference_data_item in enumerate(reference_data):
            words_ref = reference_data_item[0]

            if word_res in words_ref:
                vector[word_res] = position_ref - position_res
                break
            else:
                vector[word_res] = len(reference_data)

    length = np.sqrt(np.sum(v ** 2 for v in vector.values())) / len(reference_data)
    return length


def prepare_result_data(result_f):
    data = []
    max_val = 0
    for row in result_f:
        d = row.strip().split()
        word = d[0].lower()
        val = float(d[1])

        max_val = val if val > max_val else max_val

        data.append((val, word))
    return [(words, float(val) / max_val) for (val, words) in data]


def prepare_reference_data(reference_f):
    reference_data_reader = csv.reader(reference_f)
    reference_data = []

    max_val = 0
    for row in reference_data_reader:
        val = int(row[0])
        max_val = val if val > max_val else max_val
        words = [word.lower() for word in row[1].split(",")]
        reference_data.append((val, words))

    return [(words, float(val) / max_val) for (val, words) in reference_data]


result_data_path = "../data/results"
comparator = position_comparator
# comparator = basic_comparator


def run():
    folders = os.listdir(result_data_path)

    for name in folders:
        current_result_dir = result_data_path + "/" + name

        print(name)

        for stimuli in stimuli_words:
            length = compare(stimuli, current_result_dir, comparator=comparator)
            # print("{}: {:.3f}".format(stimuli, length))
            print("{:.3f}".format(length))

        print()


run()
