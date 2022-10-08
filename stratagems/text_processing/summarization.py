import string

def extract_data(table, tags: list, attribute: str = 'text'):
    data = []
    for tag in tags:
        values = list(table[table['tags'] == tag][attribute])
        data.extend(values)
    return data


def filter(text: str) -> list:
    punct = string.punctuation
    prep = ['без', 'безо', 'близ', 'в', 'во', 'вместо', 'вне', 'для', 'до', 'за'\
            , 'из', 'изо', 'из-за', 'из-под', 'к', 'ко', 'кроме', 'между', \
            'меж', 'на', 'над', 'о', 'об', 'обо', 'от', 'ото', 'перед', \
            'передо', 'пред', 'пред', 'пo', 'под', 'подо', 'при', 'про',\
            'ради', 'с', 'со', 'сквозь', 'среди', 'у', 'через', 'чрез', \
            'как', 'и', 'a', 'это',]
    alphabet = ''.join([chr(i) for i in range(1072, 1072 + 32)])
    sentences = []
    for sentence in text.split('.'):
        _words = []
        sentence = sentence.lower()
        for word in sentence.split():
            if word.isdigit() or word in prep:
                continue
            elif punct in word:
                word = word[:-1]
            word = word.lower()
            for letter in word:
                if letter not in alphabet:
                    break
            else:
                _words.append(word)
        if _words:
            sentences.append(_words)
    return sentences


def general_words(sentences: list) -> list:
    gwords = set()
    for i in range(len(sentences) - 1):
        current_sentence = sentences[i]
        for word in current_sentence:
            if word in sentences[i + 1]:
                gwords.add(word)
    return list(gwords)


def clossest(filetered_text: list) -> list:
    gwords = general_words(filetered_text)
    out = []
    for i in range(len(filetered_text)):
        sentence = filetered_text[i]
        count = 0
        for word in sentence:
            if word in gwords:
                count += 1
        out.append(count / len(sentence))
    return out


def summarization(text: str, weights: list, best_of: int = 3):
    out = []
    sentences = text.split('.')
    for i in range(best_of):
        if weights is None or len(weights) == 0:
            return out
        index = weights.index(max(weights, default=0))
        out.append(sentences[index + i])
        weights.pop(index)
    return out

"""Пример"""
if __name__ == '__main__':
    text = """Доля потребительских кредитов по количеству выданных ссуд на рынке розничного кредитования
    упала по итогам 2012 года ниже 70 процентов. Об этом сообщает РИА Новости со ссылкой на данные пресс-службы
    Национального бюро кредитных историй (НБКИ). На 1 января 2013 года доля выданных потребительских займов 
    составила 69,49 процента, тогда как годом ранее достигала 73,35 процента. При этом, как отмечают специалисты НБКИ,
    самым быстрорастущим видом кредитования в прошлом году стало получение займов с помощью кредитных карт.
    По итогам 2012 года число выданных ссуд с помощью кредитных карт увеличилось на 74,81 процента. 
    Для сравнения, в 2011 году рост данного показателя составил 44,77 процента. На втором месте по динамике после
    займов по кредиткам оказалось ипотечное кредитование. Число подобных ссуд за 2012 год выросло на 50,53 процента
    (годом ранее - на 35,44 процента). Потребительские кредиты и ссуды на покупку автомобиля показали рост в 36,94 и
    36,71 процента соответственно (в 2011 году - 32,67 и 33,15 процента). В НБКИ считают, что высокие темпы
    кредитования в России являются положительным фактором, "отражающим зрелость рынка и повышение его технологичности
    и ответственности". В НБКИ ожидают, что в 2013 году рынок розничного кредитования увеличится на 25-30 процентов.
    В ЦБ ранее прогнозировали, что объем корпоративных кредитов в текущем году вырастет на 15 процентов,
    потребительских - на 20-30 процентов. При этом в регуляторе обеспокоены ростом потребкредитования в России,
    указывая, что увеличение задолженности по таким ссудам может стать угрозой для финансовой устойчивости страны."""
    filtered_text = filter(text)
    weigths = clossest(filtered_text)
    print(summarization(text, weigths))

