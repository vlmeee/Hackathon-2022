import requests
from bs4 import BeautifulSoup


def parse_news():
    news_list = []

    url = "https://vc.ru/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find_all("div", class_="feed__chunk")

    for container in news_container:
        container_detail = container.find_all("div", class_="content content--short")
        for item in container_detail:
            news_text_link = item.find("a", class_="content-link")

            item = item.find("div", class_="content-container")
            if item is None:
                continue

            news_detail_dict = {}
            news_title = item.find("div", class_="content-title content-title--short l-island-a")
            news_snippet = item.find("p")
            news_title = news_title.string

            if not news_title is None:
                news_detail_dict["news_title"] = news_title.strip()
            if not news_snippet is None:
                news_snippet = news_snippet.get_text()
                news_detail_dict["news_snippet"] = news_snippet
            if news_text_link is not None:
                news_text_link = news_text_link.get("href")
                if news_text_link is not None:
                    news_detail_dict["news_text"] = parse_text_from_article_vcru(
                        news_text_link
                    )

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


def parse_text_from_article_vcru(article_url):
    full_article_text = ''

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article_container = soup.find('div', class_='content content--full')

    for paragraph in article_container.find_all('div', class_='l-island-a'):
        for p_tag in paragraph.find_all('p'):
            full_article_text += ' '.join(p_tag.stripped_strings) + '\n'

    return full_article_text



