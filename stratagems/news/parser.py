import requests
from bs4 import BeautifulSoup


def parse_news():
    news_list = []

    url = "https://vc.ru/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find_all("div", class_="content-container")

    for item in news_container:
        news_detail_dict = {}
        news_title = item.find("div", class_="content-title content-title--short l-island-a")
        news_snippet = item.find("div", class_="l-island-a")
        news_title = news_title.string
        if not news_title is None:
            news_detail_dict["news_title"] = news_title.strip()
        news_snippet = news_snippet.string
        if not news_title is None:
            news_detail_dict["news_snippet"] = news_snippet.strip()
        news_list.append(news_detail_dict)
    # result = soup.find_all("div", class_="content-title content-title--short l-island-a")
    # print(result)
    return news_list