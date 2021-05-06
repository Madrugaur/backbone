import bs4
import requests
from download_pages import start_save_process, get_tags
import traceback

root_url = "https://en.wikipedia.org/wiki/Category:Lists_of_people_in_STEM_fields"
base_url = "https://en.wikipedia.org"

# Might remove in favor having this redundancy filtering being done at download
have_visited = dict()

pages_to_ignore = []

headings_to_ignore = ["Editing:", "Portal:", "Wikipedia:", "Talk:", "File:", "Template:"]


def descend(page, level: int, is_redirect=False):
    try:
        if level >= 4:
            return
        if page is not None:
            heading = page.find(id="firstHeading")
            heading_text = heading.text
            if heading_text in pages_to_ignore:
                return
            elif page in have_visited.keys():
                return
            elif [element for element in headings_to_ignore if (element in heading_text)]:
                return
            else:
                print("\n|", 2 * level * "—", heading_text, sep="", end="")
                if "Category" in heading_text:
                    handle_category(page, level + 1)
                elif "Lists of" in heading_text and not is_redirect:
                    handle_lists(page, level + 1)
                elif "List of" in heading_text and not is_redirect:
                    handle_list(page, level + 1)
                else:
                    handle_ambiguous_page(page, level + 1)

    except Exception as e:
        print("")
        print(e)


def handle_ambiguous_page(page, level):
    biography_infobox = page.find(class_="infobox biography vcard")

    if biography_infobox is not None or prob_is_a_person(page):
        have_visited[page] = True
        start_save_process(page)
        print(": Saved", end="")
        return


def prob_is_a_person(page):
    tags = get_tags(page)
    str_tags = " ".join(tags)
    personhood_markers = ["living ", " births", " deaths"]
    for marker in personhood_markers:
        if marker in str_tags.lower():
            return True
    return False


def handle_category(page, level: int):
    sub_pages = page.find(id="mw-pages")
    list_items = sub_pages.find_all("li")
    for item in list_items:
        have_visited[page] = True
        link = item.find("a")
        url = base_url + link["href"]
        descend(get_bs4_page(url), level)


def handle_lists(page, level: int):
    content = page.find(class_="mw-parser-output")
    list_items = content.find_all("li")
    for list_item in list_items:
        have_visited[page] = True
        link = list_item.find("a")
        url = base_url + link["href"]
        descend(get_bs4_page(url), level)


def handle_list(page, level: int):
    content = page.find(class_="mw-parser-output")
    if content is None:
        return
    link_to_pages = content.find_all("a")
    for link in link_to_pages:
        href = link["href"]
        is_redirect = False
        if link.has_attr("class"):
            is_redirect = ("mw-redirect" in link["class"])
        if ("#" not in href) and (link.text != "link") and ("List of" not in link.text) \
                and ("Lists of" not in link.text) and ("Category" not in link.text):
            have_visited[page] = True
            descend(get_bs4_page(base_url + href), level, is_redirect)


def get_bs4_page(url: str):
    if "/wiki/" not in url:
        return None
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, "html.parser")


if __name__ == '__main__':
    descend(get_bs4_page(root_url), 0)
