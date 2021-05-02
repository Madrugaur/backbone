import json
import os


def calc_gender_dist():
    files = os.listdir("data/people")

    gender_dist_dict = {
        "male": 0,
        "female": 0,
        "ambiguous": 0
    }

    for f in files:
        with open("data/people/" + f, "r", encoding="utf8") as file:
            person_dict = json.load(file)
            gender_dist_dict[person_dict["gender"]] += 1

    with open("data/stats/overall_gender_dist.txt", "w", encoding="utf8") as data_file:
        data_file.write(f"male: {gender_dist_dict['male']}\nfemale: {gender_dist_dict['female']}\nambiguous: {gender_dist_dict['ambiguous']}")


if __name__ == '__main__':
    calc_gender_dist()
