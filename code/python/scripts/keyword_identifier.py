import math

from scipy.stats.distributions import chi2
import os
import json

from google_ngram_api import NGramRequest


def find_all_keys(data):
    keys = set()
    for data_dict in data:
        for key in data_dict["counts"].keys():
            if data_dict["counts"][key] > 10:
                keys.add(key)
    return keys


def find_relative_keywords(a_dict, b_dict):
    keywords = set()
    for key in a_dict:
        if key in b_dict:
            a_freq = math.log(a_dict[key])
            b_freq = math.log(b_dict[key])
            lr = likelihood_ratio(a_freq, b_freq)
            p = chi2.sf(lr, 1)
            if p < 0.001:
                keywords.add(key.lower())
    return keywords


def find_freq_by_gender(data):
    f_keys = find_all_keys(filter(lambda item: item["gender"] == "female", data))
    m_keys = find_all_keys(filter(lambda item: item["gender"] == "male", data))
    m_dict = dict()
    f_dict = dict()
    for d_dict in data:
        for key in d_dict["freq"].keys():
            if key in f_keys:
                f_dict[key] = d_dict["freq"][key]
            if key in m_keys:
                m_dict[key] = d_dict["freq"][key]
    f_keywords = find_relative_keywords(f_dict, m_dict)
    m_keywords = find_relative_keywords(m_dict, f_dict)
    print("-------f_keywords\n", "\n".join(f_keywords))
    print("-------m_keywords\n", "\n".join(m_keywords))


def find_aggregate_freq(data):
    agg_freq = dict()
    count_dict = dict()
    keys = find_all_keys(data)
    for key in keys:
        for data_dict in data:
            l_key = key.lower()
            if key in data_dict["freq"].keys():
                if l_key in agg_freq.keys():
                    agg_freq[l_key] += data_dict["freq"][key]
                    count_dict[l_key] += 1
                else:
                    agg_freq[l_key] = data_dict["freq"][key]
                    count_dict[l_key] = 1
    for key in agg_freq.keys():
        agg_freq[key] /= count_dict[key]

    return agg_freq


def likelihood_ratio(llmin, llmax):
    return 2 * (llmax - llmin)


def get_data():
    files = os.listdir("data/people/")
    data = []
    for f in files:
        with open("data/people/" + f, "r", encoding="utf8") as file:
            data.append(json.load(file))
    return data


def find_aggregate_keywords():
    data = get_data()
    with open("data/aggregate_frequency.json", "r", encoding="utf8") as file:
        agg_freq = json.load(file)
        key_words = set()
        for person_data in data:
            for word in person_data["freq"].keys():
                if word.lower() in agg_freq.keys():
                    local_freq = math.log(person_data["freq"][word])
                    act_freq = math.log(agg_freq[word.lower()])
                    lr = likelihood_ratio(local_freq, act_freq)
                    p = chi2.sf(lr, 1)
                    if p < 0.001:
                        key_words.add(word)
        with open("data/aggregate_keywords.txt", "w", encoding="utf8") as keyword_file:
            for key in key_words:
                keyword_file.write(key + "\n")


def find_global_keywords(data):
    key_words = set()
    with open("data/aggregate_frequency.json", "r", encoding="utf8") as file:
        agg_dict = json.load(file)
        keys = list(agg_dict.keys())
        global_freqs = list()
        step = 900
        for chunk in range(step, len(keys), step):
            search_str = ",".join(keys[chunk - step: chunk])
            retrieved = NGramRequest(search_str, start_year=2018).getJSON()
            global_freqs.append(retrieved)
        with open("data/global_freqs.json", "w", encoding="utf8") as g_freqs_file:
            g_freqs_file.write(json.dumps(global_freqs, indent=4))
        for ngram in global_freqs:
            g_word = ngram['ngram']
            g_freq = ngram['timeseries'][-1]
            if g_freq != 0:
                g_ll = math.log(g_freq)
                local_ll = math.log(agg_dict[g_word])
                lr = likelihood_ratio(local_ll, g_ll)
                p = chi2.sf(lr, 1)
                if p < 0.001:
                    print(g_word)
                    key_words.add(g_word)
    print("\n".join(key_words))


if __name__ == '__main__':
    find_global_keywords(get_data())
    # find_freq_by_gender(get_data())
    # find_aggregate_keywords()
