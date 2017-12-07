import pickle

# http://citeseerx.ist.psu.edu/viewdoc/download;jsessionid=3A220073CE054642A64421CFC7A59740?doi=10.1.1.47.846&rep=rep1&type=pdf

# data = data_loader.load('data/stimuli/lisc.csv')
# print(data)
from collections import defaultdict


def load_basic_form_texts(filename):
    with open("work/"+filename, "rb") as file:
        texts_basic_forms = pickle.load(file)
    return texts_basic_forms


def get_word_ranking():
    counts = defaultdict(int)
    for word in corpus_bf:
        counts[word] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def get_stopwords(ordered_counts, stopwords_percent_of_all):
    percent_of_all = 0
    stop_words = []
    for word, count in ordered_counts:
        percent_of_all += count / len(corpus_bf)
        stop_words.append(word)

        if percent_of_all >= stopwords_percent_of_all:
            break
    return stop_words


def remove_stop_words(corpus, stop_list):
    return [word for word in corpus if word not in stop_list]


stimuli_words = ['kwiat', 'liść', 'łodyga', 'roślina']

corpus_bf = load_basic_form_texts("pap.p")
ordered_counts = get_word_ranking()
stop_list = get_stopwords(ordered_counts, stopwords_percent_of_all=0.25)
corpus_bf = remove_stop_words(corpus_bf, stop_list)

# x = defaultdict(int)
# for word in corpus_bf:
#     if word in stimuli_words:
#         x[word] += 1
#
# print(x)



