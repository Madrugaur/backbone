import bs4
import requests
from download_pages import start_save_process
from multiprocessing import Queue
root_url = "https://en.wikipedia.org/wiki/List_of_people_considered_father_or_mother_of_a_scientific_field"
base_url = "https://en.wikipedia.org"

# Might remove in favor having this redundancy filtering being done at download
have_visited = dict()

pages_to_ignore = ["List of people considered father or mother of a field"]


def descend(page):
    try:
        if page is not None:
            heading = page.find(id="firstHeading")
            heading_text = heading.text
            if heading_text in pages_to_ignore:
                return
            elif page in have_visited.keys():
                return
            elif "Editing" in heading_text:
                return
            elif "Portal" in heading_text:
                return
            elif "Category" in heading_text:
                handle_category(page)
            elif "Lists of" in heading_text:
                handle_lists(page)
            elif "List of" in heading_text:
                handle_list(page)
            else:
                handle_ambiguous_page(page)
    except Exception as e:
        print(e)


def handle_ambiguous_page(page):
    biography_infobox = page.find(class_="infobox biography vcard")
    if biography_infobox is not None:
        have_visited[page] = True
        start_save_process(page)
        return


def handle_category(page):
    sub_pages = page.find(id="mw-pages")
    links_to_subpages = sub_pages.find_all("li")
    for link in links_to_subpages:
        have_visited[page] = True
        url = base_url + link["href"]
        descend(get_bs4_page(url))


def handle_lists(page):
    content = page.find(class_="mw-parser-output")
    list_items = content.find_all("li")
    for list_item in list_items:
        have_visited[page] = True
        link = list_item.find("a")
        url = base_url + link["href"]
        descend(get_bs4_page(url))


def handle_list(page):
    content = page.find(class_="mw-parser-output")
    if content is None:
        return
    link_to_pages = content.find_all("a")
    for link in link_to_pages:
        href = link["href"]
        if "#" not in href:
            have_visited[page] = True
            descend(get_bs4_page(base_url + href))


def get_bs4_page(url: str):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, "html.parser")


if __name__ == '__main__':
    descend(get_bs4_page(root_url))
