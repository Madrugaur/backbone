import bs4
import os
import json

json_template = """
{
"name": "{name},
"content": "{content}",
"tags": "{tags}",
"raw": "{raw}"
}
"""


def start_save_process(page):
    page_name = page.find(id="firstHeading").text
    json_obj = {
        "name": page_name,
        "content": get_content(page),
        "tags": get_tags(page),
        "raw": page.find(class_="mw-parser-output").text
    }

    f_name = os.path.join(os.getcwd(), "data/people/people_" + page_name + ".txt")
    f = open(f_name, "w", encoding="utf8")
    f.write(json.dumps(json_obj))


def get_tags(page):
    category_box = page.find(id="catlinks")
    list_of_category_items = category_box.find_all("li")
    str_tag_list = list()
    for item in list_of_category_items:
        link = item.find("a")
        str_tag_list.append(link.text)
    return str_tag_list


def get_content(page):
    raw_content = page.find(class_="mw-parser-output")
    paragraphs = raw_content.find_all("p")
    content = ""
    for p in paragraphs:
        content += p.text + " "
    return content
