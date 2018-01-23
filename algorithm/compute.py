import os
import pickle
from collections import defaultdict
from operator import itemgetter
from pprint import pprint

from algorithm.timer import Timer

stimuli_words = ["kwiat", "liść", "łodyga", "roślina"]

Hij_search_ranges = [8]

alphas = [0.66]
betas = [2e-5]
gammas = betas

top_collocations = 25


def run():
    with Timer("load data"):
        dict = load_data("dict.pickle")
        rdict = load_data("rdict.pickle")
        text = load_data("filtered_text.pickle")

    stimuli_word_ids = get_stimuli_word_ids(dict)

    with Timer("compute r(i, j) for given parameters"):
        compute_r_ij_for_given_parameters(rdict, stimuli_word_ids, text)


def compute_r_ij_for_given_parameters(rdict, stimuli_word_ids, text):
    for Hij_search_range in Hij_search_ranges:

        with Timer("compute H(j) and H(i&j), range={}".format(Hij_search_range)):
            Hj, Hij = compute_Hj_and_Hij(stimuli_word_ids, text, Hij_search_range)

        for _alpha in alphas:
            for _beta in betas:
                for _gamma in gammas:
                    r_ij = compute_r_ij(Hij, Hj,
                                        stimuli_word_ids, text,
                                        _alpha, _beta, _gamma)

                    save_results(_alpha, _beta, _gamma, r_ij, rdict, Hij_search_range)


def save_results(_alpha, _beta, _gamma, r_ij, rdict, Hij_search_range):
    os.makedirs("results/", exist_ok=True)

    for stimuli_word_id, r_ij_vals in r_ij.items():
        stimuli_word = rdict[stimuli_word_id]

        result = []

        os.makedirs("results/{}".format(stimuli_word), exist_ok=True)
        filename = "results/{}/range{:}_α{:.2f}_β{:.5f}_γ{:.5f}.txt" \
            .format(stimuli_word, Hij_search_range, _alpha, _beta, _gamma)

        with open(filename, "w", encoding="utf8") as f:
            print("--------------------------------", file=f)
            print(stimuli_word, file=f)
            print("--------------------------------\n", file=f)

            for (word_id, val) in r_ij_vals[:top_collocations]:
                if word_id != stimuli_word_id:
                    print("{}\t{:.4f}".format(rdict[word_id], val), file=f)
                    result.append((rdict[word_id], val))

        print(stimuli_word, "------------------------")
        pprint(result)


def load_data(pickle_fn):
    with open(pickle_fn, "rb") as f:
        data = pickle.load(f)
    return data


def compute_r_ij(Hij, Hj, stimuli_word_ids, text, alpha, beta, gamma):
    Q = len(text)

    def compute_r_ij_for_val(Hij_val, Hj_val):
        return Hij_val / pow(Hj_val, alpha) if Hj_val > beta * Q else Hij_val / (gamma * Q)

    def sort_r_ij(r_ij):
        return {k: sorted(v.items(), key=itemgetter(1), reverse=True) for k, v in r_ij.items()}

    def init_r_ij():
        return {stimuli_word_id: defaultdict(float) for stimuli_word_id in stimuli_word_ids}

    r_ij = init_r_ij()

    for (word_i_id, word_j_id), Hij_val in Hij.items():
        Hj_val = Hj[word_j_id]
        r_ij[word_i_id][word_j_id] = compute_r_ij_for_val(Hij_val, Hj_val)

    r_ij = sort_r_ij(r_ij)

    return r_ij


def compute_Hj_and_Hij(stimuli_word_ids, text, Hij_search_range):
    Hij = defaultdict(int)
    Hj = defaultdict(int)

    def compute_j_words_and_update_Hij(i, word_i_id):
        for j in get_j_range(i):
            word_j_id = text[j]
            Hij[(word_i_id, word_j_id)] += 1

    def get_j_range(i):
        it_start = i - Hij_search_range if 0 < i - Hij_search_range < len(text) else 0
        it_end = i + Hij_search_range if i + Hij_search_range < len(text) else len(text) - 1
        return range(it_start, it_end)

    for i, word_i_id in enumerate(text):
        if word_i_id in stimuli_word_ids:
            Hj[word_i_id] += 1
            compute_j_words_and_update_Hij(i, word_i_id)

    return Hj, Hij


def get_stimuli_word_ids(dict):
    return set([dict[w] for w in stimuli_words])


run()
