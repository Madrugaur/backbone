import json
import os


def read_json(f_name: str):
    with open("data/freq/" + f_name, encoding="utf8") as json_file:
        incoming_data = json.load(json_file)
    return incoming_data


def guess_gender(freq_data):
    she_count = 0
    he_count = 0
    counts = freq_data["counts"]
    if "he" in counts.keys():
        he_count += counts["he"]
    if "He" in counts.keys():
        he_count += counts["He"]
    if "she" in counts.keys():
        she_count += counts["she"]
    if "She" in counts.keys():
        she_count += counts["She"]

    if she_count > he_count:
        return 1
    elif he_count > she_count:
        return 0
    else:
        return -1


if __name__ == '__main__':
    files = os.listdir("data/freq/")
    switch = {
        0: "male",
        1: "female",
        -1: "ambiguous"
    }
    for f in files:
        data = read_json(f)
        gender_guess = guess_gender(data)
        data.update({"gender": switch[gender_guess]})
        with open("data/gender/" + f, "w+", encoding="utf8") as new_file:
            new_file.write(json.dumps(data))
