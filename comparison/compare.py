import csv

import numpy as np

stimuli_words = ["lisc", "kwiat", "lodyga", "roslina"]


def compare(stimuli, comparator):
    with open("to_compare/{}.txt".format(stimuli), "r", encoding="utf8") as result_f:
        with open("../data/stimuli/{}.csv".format(stimuli), "r", encoding="utf8") as reference_f:
            reference_data = prepare_reference_data(reference_f)
            result_data = prepare_result_data(result_f)

            length = comparator(reference_data, result_data)

    return length


def basic_comparator(reference_data, result_data, compare_count=25):
    vector = {}
    for reference_data_item in reference_data[:compare_count]:
        words_ref = reference_data_item[0]
        val_ref = reference_data_item[1]

        for result_dat_item in result_data[:compare_count]:
            word_res = result_dat_item[0]
            val_res = result_dat_item[1]

            vector[word_res] = val_ref - val_res if word_res in words_ref else val_res
    length = np.sqrt(np.sum(v ** 2 for v in vector.values()))
    return length


def position_comparator(reference_data, result_data, compare_count=25):
    vector = {}

    for position_res, result_dat_item in enumerate(result_data[:compare_count]):
        word_res = result_dat_item[0]

        for position_ref, reference_data_item in enumerate(reference_data):
            words_ref = reference_data_item[0]

            if word_res in words_ref:
                vector[word_res] = np.abs(position_ref-position_res)
                break

    length = np.sqrt(np.sum(v ** 2 for v in vector.values()))/len(reference_data)
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


def run():
    comparator = position_comparator

    for stimuli in stimuli_words:
        length = compare(stimuli, comparator=comparator)
        print("{}: {:.3f}".format(stimuli, length))


run()
