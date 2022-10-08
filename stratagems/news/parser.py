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

    # https://journal.tinkoff.ru/tag/breaking-news/

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


def parse_1c():
    ''' Парсит данные с сайта 1с. Парсит 60 страниц. Это примерно 15 октября 2020 года  '''
    news_list = []
    tags_to_delete_from_text = (
        ('div', 'social_links social_links__top'),
        ('h1', ''),
        ('ul', 'pager'),
        ('div', 'infonews_footer'),
        ('table', ''),
        ('div', 'panel featured')
    )
    for page_number in range(1, 61):
        url = f'https://1c.ru/news/newslist.jsp?partniininndnnHnsnnbnnrnnfjiCnfV350nunnsnncnnfjiCnfV350nunnnnnninnnm1n1Dinfnf={page_number}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        news_container = soup.find('ul', class_='news-list')
        for item in news_container.find_all('li'):
            for link in item.find_all('a'):
                news_detail_dict = {}
                if not link.get('href').startswith('http'):
                    link_url = 'https://1c.ru' + link.get('href')
                else:
                    link_url = link.get('href')
                if link_url is None:
                    continue
                page_link_url = BeautifulSoup(
                    requests.get(link_url).content,
                    'html.parser')
                page_text = page_link_url.find('div', class_='redhead')

                if page_text is None:
                    continue

                tmp_title = page_link_url.find(
                    'div', class_='panel featured'
                )
                if tmp_title is not None:
                    news_detail_dict['news_title'] = tmp_title.text.strip()

                tmp_snippet = page_link_url.find(
                    'p'
                )
                if tmp_snippet is not None:
                    news_detail_dict['news_snippet'] = tmp_snippet.text.strip()

                for tag, class_ in tags_to_delete_from_text:
                    for item in page_text.find_all(tag, class_=class_):
                        item.extract()
                news_detail_dict['news_text'] = page_text.text.strip()
                if news_detail_dict:
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


def parse_text_from_article_tinkoff_journal(article_url):
    full_article_text = ''

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    article_container = soup.find('div', class_='article-body')

    for paragraph in article_container.find_all('p', class_='paragraph'):
        full_article_text += ' '.join(paragraph.stripped_strings) + '\n'

    return full_article_text


if __name__ == '__main__':
    # parse_1c()
    pass