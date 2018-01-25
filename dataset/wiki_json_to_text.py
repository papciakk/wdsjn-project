import json
from sys import argv

min_len = 50

with open(argv[2], "w", encoding="utf-8") as f_out:
    with open(argv[1], "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if line == "":
                break

            json_data = json.loads(line, encoding="utf-8")
            text = " ".join(json_data['text'].split())

            if len(text) > min_len:
                print(text, end=" ", file=f_out)

