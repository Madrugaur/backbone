"""
brief: the purpose of this script is to assert there is a/are common attribute(s) attached to all of the linked
        articles under
        <a href="https://en.wikipedia.org/wiki/Index_of_women_scientists_articles">Index of Women Scientists Articles</a>
        If such an attribute or attributes exists, I can reasonably assume that it or they will apply to all of the
        articles about women in other Indices or Lists.
author: Braden Little
"""

import bs4
import requests

base_url = "https://en.wikipedia.org"

response = requests.get("https://en.wikipedia.org/wiki/Index_of_women_scientists_articles")

if response is not None:
    page = bs4.BeautifulSoup(response.text, "html.parser")
    cols = page.find_all("div", class_="div-col")

    for col in cols:
        list_elements = col.find_all("li")
        for element in list_elements:
            link = element.select("a")[0]["href"]
            subpage = bs4.BeautifulSoup(requests.get(base_url + link))
            cats = subpage.select("div", class_="catlinks")[0]
            print(cats)


