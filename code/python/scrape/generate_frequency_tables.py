import json
import os
import re


def generate():
    files = os.listdir("data/people/")
    for f in files:
        data = read_json(f)

        counts, total = calculate_counts(data["content"])

        freq = calculate_frequency(counts, total)
        sorted_freq = sorted(freq.items(), key=lambda i: i[1])
        sorted_freq.reverse()
        data.update(counts)
        data.update(freq)
        data.update({"total": total})
        file = open("data/freq/" + f, "w", encoding="utf8")
        file.write(json.dumps(data))


def calculate_counts(content: str):
    table = dict()
    total = 0
    for word in content.split(sep=" "):
        c_word = clean_word(word)
        if len(c_word) != 0:
            total += 1
            if c_word in table.keys():
                table[c_word] += 1
            else:
                table[c_word] = 1
    return table, total


def calculate_frequency(counts, total):
    freq = dict()
    for count in counts.items():
        freq[count[0]] = count[1] / total
    return freq


def clean_word(word: str):
    to_remove = r"[,@\'?\.$%_\d\W]"
    return re.sub(to_remove, "", word)


def read_json(f_name: str):
    with open("data/people/" + f_name, encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    generate()