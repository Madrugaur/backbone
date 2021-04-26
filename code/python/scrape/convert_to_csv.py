# compile a list of unique words from all files
# write each person as a rows in the csv
# HEADER
# person_name, person_gender, page_word_count, person_tags, .... [all unique words]

import os
import json
import csv


def find_all_unique_words():
    master_word_list = set()
    files = os.listdir("data/freq/")
    for file in files:
        with open("data/gender/" + file, encoding="utf8") as json_file:
            incoming_data = json.load(json_file)
            master_word_list |= incoming_data["counts"].keys()
    return master_word_list


if __name__ == '__main__':
    header = {"person_name", "person_gender", "page_word_count"} | find_all_unique_words()
    with open("data/aggregate_data.csv", "w+", encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
