## Ваша задача построить сеть для произвольного семантического поля, 
## где узлами будут слова, а ребрами наличие косинусного расстояния больше 0.5 в word2vec-модели. 
## Вычислите самые центральные слова графа, его радиус (для каждой компоненты связности) и коэффициент кластеризации.
## Наше семантическое поле - сверхъестественные существа (как русской, так и западной традиции)

import sys
import gensim, logging
import matplotlib.pyplot as plt
import networkx as nx


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


## Тренируем модель
def model_creator():
    m = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    if m.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(m)

    model.init_sims(replace=True)
    return model


def semantic_field(model, words):
    G = nx.Graph()
    for word in words:
        if word + '_NOUN' in model:
            G.add_node(word)
    return G


## Задаем узлы графа
def nodes(model, words):
    G = semantic_field(model, words)
    for word in words:
        extra_node = word + '_NOUN'
        if extra_node in G:
            G.remove_node(extra_node)
    return G


## Задаем ребра графа и сохраняем его
def edges(model, G):
    nodelist = G.nodes()
    for first_node in nodelist:
        n_1 = first_node + '_NOUN'
        for second_node in nodelist:
            n_2 = second_node + '_NOUN'
            if second_node != first_node:
                sim = model.similarity(n_1, n_2)
                if sim > 0.5:
                    G.add_edge(first_node, second_node, weight=sim)

    nx.write_gexf(G, 'supernatural.gexf')


## Визуализируем граф в matplotlib
def graph_maker(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color = '#98eff9', node_size = 50)
    nx.draw_networkx_edges(G, pos, edge_color = '#06470c') 
    nx.draw_networkx_labels(G, pos, font_size = 15, font_family = 'Georgia')
    plt.axis('off')
    plt.show()
    

## Вычислим 10 центральных слов
def central_words(G):
    print('Центральные слова графа:')
    degree = nx.degree_centrality(G)
    i = 0
    for nodeid in sorted(degree, key=degree.get, reverse = True):
        if i <= 10:
            i += 1
            print(nodeid)


## Вычислим коэффициент кластеризации
def clusterization(G):
    print('Коэффициент кластеризации графа:')
    print(nx.average_clustering(G))


## Вычислим радиус графа для каждой компоненты связности
def radius(G):
    for component in nx.connected_components(G):
        sub_G = G.subgraph(component)
        print(str(component) + ' : ' + str(nx.radius(sub_G)))
    

def main():
    words = ['тварь', 'существо', 'создание', 'черт', 'чертик', 'чертенок', 'Дьявол',
             'дьявол', 'дьяволенок', 'дьяволица', 'демон', 'Сатана', 'ангел', 'серафим',
             'фея', 'эльф', 'гоблин', 'орк', 'гном', 'вампир', 'вурдалак', 'упырь',
             'русалка', 'ведьма', 'колдун', 'водяной', 'кикимора', 'леший', 'Баба Яга',
             'призрак', 'привидение', 'полтергейст', 'бес', 'Бог', 'бог', 'божество',
             'дух', 'Архангел', 'сирена', 'зомби', 'домовой', 'дракон', 'единорог',
             'феникс', 'оборотень', 'монстр', 'нефилим', 'джинн', 'голем']
    model = model_creator()
    G =  nodes(model, words)
    edges(model, G)
    graph_maker(G)
    central_words(G)
    clusterization(G)
    radius(G)


if __name__ == "__main__":
    main()
    
## Результаты:

## Центральные слова графа:
## ведьма
## дьяволица
## дьявол
## вурдалак
## колдун
## кикимора
## демон
## оборотень
## леший
## привидение
## ангел

## Коэффициент кластеризации графа:
## 0.329616724738676

## Радиус:
## {'призрак', 'вампир', 'кикимора', 'эльф', 'вурдалак', 'оборотень', 'зомби', 'водяной', 'ведьма', 'дьяволица', 'демон', 'гном', 'ангел', 'черт', 'орк', 'леший', 'чертенок', 'привидение', 'бес', 'гоблин', 'русалка', 'серафим', 'колдун', 'дьявол', 'упырь', 'фея'} : 3
## {'сирена'} : 0
## {'существо', 'божество', 'тварь', 'бог'} : 1
## {'домовой'} : 0
## {'дух'} : 0
## {'создание'} : 0
## {'полтергейст'} : 0
## {'джинн'} : 0
## {'монстр'} : 0
## {'дракон', 'единорог'} : 1
## {'чертик'} : 0
## {'феникс'} : 0
