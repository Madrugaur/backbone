import bs4
import os


def start_save_process(page):
    page_name = page.find(id="firstHeading").text
    f_name = os.path.join(os.getcwd(), "data/people/people_" + page_name + ".txt")
    f = open(f_name, "w", encoding="utf8")
    f.write(page.find(class_="mw-parser-output").text)
    print(f_name)



