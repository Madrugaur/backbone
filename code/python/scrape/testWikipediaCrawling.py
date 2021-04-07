import bs4
import requests

root_url = "https://en.wikipedia.org/wiki/Category:Lists_of_people_in_STEM_fields"
base_url = "https://en.wikipedia.org"

have_visited = dict()


def descend(page):
    body = page.find(id="mw-content-text")
    links = body.find_all("li")
    links = filter(link_filter, links)
    for element in links:
        print(element)
        new_url = base_url + element["href"]
        if new_url not in have_visited.keys():
            have_visited[new_url] = True
            descend(get_bs4_page(new_url))

    pass


def link_filter(element):
    to_exclude = ["/wiki/portal:", "/wiki/category:", "/wiki/file:",
                  "/wiki/science,_technology,_engineering,_and_mathematics", "/wiki/engineer", "/wiki/wikipedia:",
                  "/wiki/help", "/wiki/european_engineer"]
    need = [""]
    if element.has_attr("class"):
        if "mw-redirect" in element["class"]:
            return False
    for item in to_exclude:
        if item in element["href"].lower():
            return False
    return True


def get_bs4_page(url: str):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text, "html.parser")


if __name__ == '__main__':
    descend(get_bs4_page(root_url))
