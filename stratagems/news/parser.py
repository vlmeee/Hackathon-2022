import requests
import json
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
            news_title = news_title.string

            if not news_title is None:
                news_detail_dict["news_title"] = news_title.strip()
            if news_text_link is not None:
                news_text_link = news_text_link.get("href")
                if news_text_link is not None:
                    news_detail_dict["news_text"] = parse_text_from_article_vcru(
                        news_text_link
                    )

            if len(news_detail_dict) != 0:
                news_list.append(news_detail_dict)
    return news_list


def parse_tinkoff_journal(full = False):

    if full == True:
        pages_amount_1 = 8
        pages_amount_2 = 42
    else:
        pages_amount_1 = 2
        pages_amount_2 = 2

    news_list = []

    category_pages_amount = {
        'Инвестиции': {
            'pages_amount': pages_amount_1,
            'url': 'https://journal.tinkoff.ru/flows/invest/page/'
        },
        'Бизнес': {
            'pages_amount': pages_amount_2,
            'url': 'https://journal.tinkoff.ru/flows/business-all/page/'
        },
    }

    for category in category_pages_amount:
        for page_number in range(1, category_pages_amount[category]['pages_amount'] + 1):
            url = category_pages_amount[category]['url'] + str(page_number)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            news_container = soup.find_all("div", class_="item--HDDKc")

            for item in news_container:
                news_detail_dict = {}
                news_title = item.find("h3", class_="title--gosKP")

                if not news_title is None:
                    news_title = news_title.string
                    if len(news_title) > 0:
                        news_detail_dict["news_title"] = news_title.strip()
                news_text_link = item.find('a', class_='link--xmoGM')
                if news_text_link is not None:
                    news_text_link = news_text_link.get('href')
                    if news_text_link is not None:
                        news_detail_dict['news_text'] = parse_text_from_article_tinkoff_journal(
                            'https://journal.tinkoff.ru' + news_text_link)
                if len(news_detail_dict) != 0:
                    news_list.append(news_detail_dict)

    return news_list


def parse_1c(full = False):
    ''' Парсит данные с сайта 1с. Парсит 60 страниц. Это примерно 15 октября 2020 года  '''
    news_list = []
    if full == True:
        page_num = 61
    else:
        page_num = 2

    tags_to_delete_from_text = (
        ('div', 'social_links social_links__top'),
        ('h1', ''),
        ('ul', 'pager'),
        ('div', 'infonews_footer'),
        ('table', ''),
        ('div', 'panel featured')
    )
    for page_number in range(1, page_num):
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


# для новостей 3-х летней давности рекомендуется pages_num = 1000
def parse_banki_ru(full_parse = False, url = "https://www.banki.ru/news/lenta/", pages_num = 5):
    news_list = []
    main_url = 'https://www.banki.ru'
    # url = "https://www.banki.ru/news/lenta/"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    news_container = soup.find_all("a", class_="lf473447f")

    for item in news_container:
        news_detail_dict = {}
        # print(item)
        if item is None:
            continue
        news_title = item.string
        news_link = main_url + item.get("href")
        # print(news_link)
        news_text = parse_banki_ru_detail(news_link)
        news_detail_dict['news_title'] = news_title
        news_detail_dict['news_text'] = news_text

        if len(news_detail_dict) != 0:
            news_list.append(news_detail_dict)

    if full_parse == True:
        page_no = 2
        while page_no < pages_num:
            print(page_no)
            url = 'https://www.banki.ru/news/lenta/?page=' + str(page_no)
            news_list_additional = parse_banki_ru(False, url)
            for item in news_list_additional:
                news_list.append(item)
            page_no = page_no + 1
    # print(len(news_list))

    return news_list


def parse_banki_ru_detail(url):
    text = ''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text_list = soup.find_all("div", class_='l6d291019')
    for item in text_list:
        p_list = item.find_all('p')
        if p_list is None:
            continue
        for internal_p_list in p_list:
            if internal_p_list is None:
                continue
            for p in internal_p_list:
                if p is None:
                    continue
                # print(p)
                text = text + str(p.string).strip()
    # print(text)
    return text



def parse_rbc():
    news_list = []
    url_list = ['https://www.rbc.ru/national',
                'https://www.rbc.ru/neweconomy/?utm_source=topline',
                'https://www.rbc.ru/economics/?utm_source=topline',
                'https://www.rbc.ru/business/?utm_source=topline',
                'https://www.rbc.ru/finances/?utm_source=topline']

    def parse_rbc_section(url):
        news_list_internal = []
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        news_container = soup.find_all("a", class_="item__link")

        for item in news_container:
            news_detail_dict = {}

            if item is None:
                continue

            if item.span.span.string is not None:
                news_title = item.span.span.string.strip()

            news_link = item.get("href")
            news_text = parse_rbc_detail(news_link)

            if news_title is not None:
                news_detail_dict['news_title'] = str(news_title)

            if news_text is not None:
                news_detail_dict['news_text'] = str(news_text)

            if len(news_detail_dict) != 0:
                news_list_internal.append(news_detail_dict)

        return news_list_internal

    for url in url_list:
        parse_rbc_section_result = parse_rbc_section(url)

        for item in parse_rbc_section_result:
            if item is not None:
                news_list.append(item)

    return news_list

def parse_rbc_detail(url):
    text = ''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text_list = soup.find_all("div", class_='article__text article__text_free')

    for item in text_list:
        p_list = item.find_all('p')

        if p_list is None:
            continue

        for internal_p_list in p_list:
            if internal_p_list is None:
                continue

            for p in internal_p_list:
                if p is None:
                    continue

                text = text + str(p.string).strip()

    return text


def parse_all(full = False):
    news_list = []

    parse_news_res = parse_news()
    parse_tinkoff_journal_res = parse_tinkoff_journal(full)
    parse_1c_res = parse_1c(full)
    parse_banki_ru_detail = parse_banki_ru(full)
    parse_rbc_res = parse_rbc()

    news_list.extend(parse_news_res)
    news_list.extend(parse_tinkoff_journal_res)
    news_list.extend(parse_1c_res)
    news_list.extend(parse_banki_ru_detail)
    news_list.extend(parse_rbc_res)

    return news_list

if __name__ == '__main__':
    # print(*(i['news_title'] for i in parse_tinkoff_journal()), sep='\n')
    with open("dataset.json", "w") as f:
        json.dump({"dataset": parse_tinkoff_journal()}, f)
        # data = json.load(f)
        # print(data['dataset'][0]['news_text'])
