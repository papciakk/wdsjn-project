import re


def not_hyperlink(word):
    return not word.__contains__("http://")


def load(filename):
    corpus = []
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            words = line.split()

            for word in words:
                word = word.lower()
                if not_hyperlink(word):
                    word = re.sub("[^a-zęóąśłżźćń]", "", word)

                    if len(word) > 0:
                        corpus.append(word)

    return corpus

