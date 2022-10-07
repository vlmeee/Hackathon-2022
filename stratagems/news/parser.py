import requests
from bs4 import BeautifulSoup


def parse_news():
    news_list = []

    url = "https://vc.ru/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find_all("div", class_="feed__chunk")

    for container in news_container:
        container_detail = container.find_all("div", class_="content-container")
        for item in container_detail:
            news_detail_dict = {}
            news_title = item.find("div", class_="content-title content-title--short l-island-a")
            news_snippet = item.find("p")
            news_title = news_title.string
            if not news_title is None:
                news_detail_dict["news_title"] = news_title.strip()
            if not news_snippet is None:
                news_snippet = news_snippet.get_text()
                news_detail_dict["news_snippet"] = news_snippet
            if len(news_detail_dict) != 0:
                news_list.append(news_detail_dict)
    return news_list


def parse_tinkoff_journal():
    news_list = []

    url = "https://journal.tinkoff.ru/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find_all("div", class_="inner--BbvB6")

    for item in news_container:
        news_detail_dict = {}
        news_title = item.find("h3", class_="title--hhlgn")

        if not news_title is None:
            news_title = news_title.string
            if len(news_title) > 0:
                news_detail_dict["news_title"] = news_title.strip()
        if len(news_detail_dict) != 0:
            news_list.append(news_detail_dict)
    return news_list
