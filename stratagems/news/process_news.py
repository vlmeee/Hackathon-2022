from .parser import parse_all
from text_processing.summarization import summarization, filter, clossest
from .models import News
from celery import shared_task
import nltk
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
nltk.download('punkt')
import nltk
nltk.download('word_tokenize')
from nltk.corpus import stopwords

from nltk.metrics.association import ContingencyMeasures


def news_summariziation(news_text):
    filtered_text = filter(news_text)
    weigths = clossest(filtered_text)

    # list of strings
    return summarization(news_text, weigths)


def determine_role(news_text):
    snowball = SnowballStemmer(language="russian")
    russian_stop_words = stopwords.words("russian")
    STOPWORDS = set(stopwords.words('russian'))
    remove_stop_words = True
    director = 'director'
    buh = 'buh'

    dircetor_words = ['бизнес', 'макроэкономик', 'рын', 'планировани', 'лидерств', 'Деньг', 'экономическ', 'минфин', 'капитал', 'казн',
     'актив', 'доход', 'сбережени', 'swot', 'рофит', 'аутсорс', 'аутсорсинг', 'инвестиционн', 'конкурентоспособн',
     'ценов', 'актив', 'рентабельн', 'инновац', 'эластичность', 'конкурентоспособн', 'инфляц', 'сбыт', 'прибыль',
     'платёжеспособн', 'производств', 'потребительск', 'спрос', 'директор', 'director', 'manager']

    buh_words = ['бухгалтер', 'законодательство', 'законодатель', 'законодател', 'ERP', 'CRM', 'Bitrix', 'bitrix',
                 'налог', 'отчётность',
                 'учет',
                 'документооборот',
                 '1С', '1с',
                 'заработн', 'зарплат',
                 'финанс',
                 'аудит',
                 'контрагент',
                 'номенклатур',
                 'автоматиз',
                 'банк',
                 'экономическ',
                 'платёж', 'платёжн',
                 'дебет', 'кредит']

    tokens_list = []

    tokens = word_tokenize(news_text, language="russian")
    tokens = [i for i in tokens if i not in string.punctuation]
    if remove_stop_words:
        tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    tokens_list.append(tokens)

    for token in tokens_list:
        if token in dircetor_words:
            return director
        elif token in buh_words:
            return buh
        else:
            return None


def insert_to_news(title, text, role):
    news = News(title=title, text=text, role=role)
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
                        role = determine_role(news_string)
                        # print(role)
                        insert_to_news(news['news_title'], news_string, role)

    return None