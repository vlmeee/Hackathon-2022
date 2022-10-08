def news_summarization(contents):
    for i in range(len(contents)):
        try:
            text = contents[i]['news_text']
            filtered_text = filter(text)
            weights = clossest(filtered_text)
            contents[i] = summarization(text, weights)
            contents[i] = filter(' '.join(contents[i]).strip())[0]
        except:
            contents[i] = ''
    return contents
def find_trend(contents, best_of = 100):
    bag_of_words = []
    for sentences in contents:
        if sentences == '':
            continue
        bag_of_words.extend(sentences)
    word_freq = Counter(bag_of_words)
    return sorted(word_freq, key=word_freq.get, reverse=True)[:best_of]

def trend_filter(hyp_trends:list)->list:
    trends = []
    for word in hyp_trends:
        if len(word) < 3:
            continue
        trends.append(word)
    return trends


if __name__ == '__main__':
    with open(json_file_path, 'r', encoding='utf-8') as j:
        contents = json.loads(j.read())['dataset']
    hyp_trends = find_trend(news_summarization(contents))
    trend = trend_filter(hyp_trends)
    #out """
    ['что',
 'компании',
 'года',
 'млрд',
 'акции',
 'если',
 'млн',
 'компания',
 'долларов',
 'все',
 'году',
 'год',
 'рублей',
 'финансовые',
 'отчет',
 'будет',
 'стр',
 'отчеты',
 'есть',
 'еще',
 'может',
 'выручки',
 'выпускают',
 'акций',
 'прибыль',
 'выручка',
 'только',
 'цена',
 'чем',
 'могут',
 'можно',
 'продажи',
 'нет',
 'сейчас',
 'более',
 'сша',
 'вам',
 'дивиденды',
 'этом',
 'вот',
 'наши',
 'прогнозы',
 'размышления',
 'выросла',
 'которые',
 'призыв',
 'действию',
 'рост',
 'квартал',
 'операционные',
 'выросли',
 'потому',
 'также',
 'уже',
 'решать',
 'полагаться',
 'американские',
 'самый',
 'доходность',
 'роста',
 'продаж',
 'сделать',
 'очень',
 'плохо',
 'после',
 'финансовый',
 'купить',
 'падает',
 'компаний',
 'квартале',
 'стоит',
 'итогам',
 'примерно',
 'годовой',
 'результаты',
 'российские',
 'прибыли',
 'прочитать',
 'всего',
 'его',
 'будут',
 'способ',
 'простой',
 'больше',
 'чтобы',
 'объем']
    """