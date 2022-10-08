import numpy as np
from numpy.linalg import norm
from navec import Navec

def text2emb(text:str, navec:Navec)->np.array:
    """
    convert sentence to sequence of embbedings
    text (str): filtered text
    output np.array: sequence of embbedings
    """
    text = filter(' '.join(text).strip())[0]
    embeddings = []
    for word in text:
        try:
          embeddings.append(navec[word])
        except:
          continue
    return np.array(embeddings)

def similar(v1, v2, threshold = .5) -> bool:
    """
    calculate cosine similarity.
    return False if cosine similarity < threshold
    """
    return np.sum((v1*v2)/(norm(v1)*norm(v2))) > threshold

def clossest_news(sum1, sum2, navec:Navec)->bool:
    """
    calclulate cosine similarity for 2 news
    """
    emb1, emb2 = text2emb(sum1, navec), text2emb(sum2, navec)
    if emb1.shape != emb2.shape:
        min_len = min(emb1, emb2, key = lambda x: x.shape[0]).shape[0]
        emb1 = emb1[:min_len]
        emb2 = emb2[:min_len]
    return similar(emb1, emb2)

if __name__ == '__main__':
    path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
    navec = Navec.load(path)
    s1 = ['В НБКИ ожидают, что в 2013 году рынок розничного кредитования увеличится на 25-30 процентов',
     'По итогам 2012 года число выданных ссуд с помощью кредитных карт увеличилось на 74,81 процента',
     'Для сравнения, в 2011 году рост данного показателя составил 44,77 процента']
    s2 = ['Goldman Sachs ожидает довольно приличных темпов роста экономики Китая в 2013 году, которые достигнут 8,1 процента',
          'Активность именно в зарубежных тратах объясняется высокими налогами на покупку роскошных товаров, существующих на основной территории Китая',
          'Если тенденция быстрого экономического роста продолжится, то объем покупок предметов роскоши внутри Китая составит в 2015 году 30 миллиардов долларов']
    clossest_news(s1, s2, navec)
    #out False