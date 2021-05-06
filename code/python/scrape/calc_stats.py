import json
import os


def calc_stats(dict_list):
    stats_dict = {
        "male": {
            "count": 0,
            "proportion": 0,
            "length": 0
        },
        "female": {
            "count": 0,
            "proportion": 0,
            "length": 0
        },
        "ambiguous": {
            "count": 0,
            "proportion": 0,
            "length": 0
        }
    }
    total = 0
    for p_dict in dict_list:
        gender = p_dict["gender"]
        stats_dict[gender]["count"] += 1
        stats_dict[gender]["proportion"] += p_dict["total"]
        total += p_dict["total"]

    for key in stats_dict.keys():
        if stats_dict[key]["count"] > 0:
            stats_dict[key]["length"] = int(stats_dict[key]["proportion"] / stats_dict[key]["count"])
            stats_dict[key]["proportion"] = percent(stats_dict[key]["proportion"] / total)

    return stats_dict


def calc_top_bottom_stats():
    files = os.listdir("data/people")
    person_list = list()
    for f in files:
        with open("data/people/" + f, "r", encoding="utf8") as file:
            person_list.append(json.load(file))
    person_list = sorted(person_list, key=lambda item: item["total"], reverse=True)

    length = len(person_list)
    bottom = list()
    top = list()

    for front in range(0, int(length * .25)):
        back = length - 1 - front
        bottom.append(person_list[back])
        top.append(person_list[front])
    return calc_stats(top), calc_stats(bottom)


def calc_word_counts():
    files = os.listdir("data/people")
    count_dict = {
        "male": 0,
        "female": 0,
        "ambiguous": 0
    }
    for f in files:
        with open("data/people/" + f, "r", encoding="utf8") as file:
            person_dict = json.load(file)
            count_dict[person_dict["gender"]] += person_dict["total"]
    return count_dict


def calc_gender_dist():
    files = os.listdir("data/people")

    dist_dict = {
        "male": 0,
        "female": 0,
        "ambiguous": 0
    }

    for f in files:
        with open("data/people/" + f, "r", encoding="utf8") as file:
            person_dict = json.load(file)
            dist_dict[person_dict["gender"]] += 1
    return dist_dict


def write_data(f_name: str, data_string):
    with open("data/stats/" + f_name, "w", encoding="utf8") as data_file:
        data_file.write(data_string)


def percent(val):
    return val * 100


if __name__ == '__main__':
    # gender_dist_dict = calc_gender_dist()
    # write_data("overall_gender_dist.txt", "male: {}\nfemale: {}\nambiguous: {}".format(gender_dist_dict['male'],
    #                                                                                   gender_dist_dict['female'],
    #                                                                                   gender_dist_dict['ambiguous']))
    # word_count_dict = calc_word_counts()
    # total_words = sum(word_count_dict.values())
    # write_data("average_word_count.txt",
    #            "male: {}\nfemale: {}\nambiguous: {}".format(calc_percent(word_count_dict['male'] / total_words),
    #                                                         calc_percent(word_count_dict['female'] / total_words),
    #                                                         calc_percent(word_count_dict['ambiguous'] / total_words)))

    top_bottom_stats = calc_top_bottom_stats()
    top = top_bottom_stats[0]
    bottom = top_bottom_stats[1]
    stats_dict = {
        "top": top,
        "bottom": bottom
    }
    write_data("top_bottom_data.txt", json.dumps(stats_dict, indent=4))
