import math

from scipy.stats.distributions import chi2
import os
import json


def likelihood_ratio(llmin, llmax):
    return 2 * (llmax - llmin)


def find_keywords():
    files = os.listdir("data/people/")
    for f in files:
        with open("data/people" + f, "r", encoding="utf8") as file:
            person_data = json.load(file)
            for word in person_data["freq"].keys():
                freq = math.log(person_data["freq"][word])
                lr = likelihood_ratio(freq, 1)
                p = chi2.sf(lr, 1)
                print('p: %.30f' % p)

if __name__ == '__main__':
    find_keywords()