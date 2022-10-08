from .parser import parse_all
from text_processing.summarization import summarization, filter, clossest
from .models import News
from celery import shared_task


def news_summariziation(news_text):
    filtered_text = filter(news_text)
    weigths = clossest(filtered_text)

    # list of strings
    return summarization(news_text, weigths)


def insert_to_news(title, text):
    news = News(title=title, text=text)
    news.save()

    return None


@shared_task(bind=True)
def process_news_and_insert(self, full = False):

    # list of dict (keys: news_title and news_text)
    news_list = parse_all(full)

    if news_list is not None:

        for news in news_list:
            news_summariziation_list = []
            news_string = ''

            if news is None:
                continue

            if 'news_text' in news and news['news_text'] is not None:
                news_summariziation_list = news_summariziation(news['news_text'])
                if len(news_summariziation_list) > 0:
                    separator = '. '
                    news_string = separator.join(news_summariziation_list)

                if 'news_title' in news:
                    if news['news_title'] is not None and news_string is not None:
                        insert_to_news(news['news_title'], news_string)

    return None