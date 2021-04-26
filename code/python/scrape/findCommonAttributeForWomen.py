"""
brief: the purpose of this script is to assert there are any Categories attached to all of the linked
        articles under
        <a href="https://en.wikipedia.org/wiki/Index_of_women_scientists_articles">Index of Women Scientists Articles</a>
        If such Categories exists, I can reasonably assume that they will apply to all of the
        articles about women in other Indices or Lists.

conclusion: Fun fact, there are no common Categories for women scientist on Wikipedia, or women in general it seems. In
        running this experiment I have discovered that there is little consistent category usage which makes my job
        much harder. So bios about women don't have any categories relating to women attached. So what I'm going to do
        is crawl through all the bios relating to people in STEM and then try to discover a reliable way of dividing
        those by gender
author: Braden Little
"""

import bs4
import requests

base_url = "https://en.wikipedia.org"

response = requests.get("https://en.wikipedia.org/wiki/Index_of_women_scientists_articles")

if response is not None:
    print("Calculating the Expected Representation of the Word 'she' in Articles about Women Scientists")
    results = list()
    page = bs4.BeautifulSoup(response.text, "html.parser")
    content_boxes = page.find_all("div", class_="div-col")
    attribute_count_map = dict()
    subpages = 0
    she_count_total = 0
    word_count_total = 0
    for content_box in content_boxes:
        people_items = content_box.find_all("li")
        for person in people_items:
            bio_link = person.select("a")[0]["href"]
            bio_page = bs4.BeautifulSoup(requests.get(base_url + bio_link).text, "html.parser")
            bio_content = bio_page.find(id="bodyContent")
            page_text = bio_content.text
            she_count = 0
            word_count = 0

            for word in page_text.split(" "):
                if "she" == word.lower():
                    she_count += 1
                word_count += 1
            she_count_total += she_count
            word_count_total += word_count
            formatted_output = bio_page.find("title").text + ": " + str((she_count / word_count) * 100) + "%"
            results.append(formatted_output)
    footer = "average representation of she pronoun: " + str((she_count_total / word_count_total) * 100) + "%\n" +\
        "total number of words read: " + str(word_count_total) + ""
    results.append(footer)
    f = open("data/she_pronoun_data.txt", "w+", encoding="utf8")
    f.write("\n".join(results))


