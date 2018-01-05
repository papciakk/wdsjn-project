import io

import os


def read_words(filename, buff_size=10240):
    file_size = os.path.getsize(filename)
    processed_size = 0

    with io.open(filename, 'r', encoding="utf8") as f:
        while True:
            buf = f.read(buff_size)
            if not buf:
                break

            while not unicode.isspace(buf[-1]):
                ch = f.read(1)
                if not ch:
                    break
                buf += ch

            words = buf.split()

            for word in words:
                yield word

            processed_size += buff_size
            print "{:.2f} %".format(float(processed_size) / file_size * 100.0)

        yield ''
