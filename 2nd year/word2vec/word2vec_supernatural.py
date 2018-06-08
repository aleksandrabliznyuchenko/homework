## Ваша задача построить сеть для произвольного семантического поля,
## где узлами будут слова, а ребрами наличие косинусного расстояния больше 0.5 в word2vec-модели.
## Вычислите самые центральные слова графа, его радиус (для каждой компоненты связности) и коэффициент кластеризации.
## Наше семантическое поле - сверхъестественные существа, как русской, так и западной традиции

import sys
import gensim, logging
import matplotlib.pyplot as plt
import networkx as nx


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


##Обучаем нашу модель
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
def edges(model, G, file):
    nodelist = G.nodes()
    for first_node in nodelist:
        n_1 = first_node + '_NOUN'
        for second_node in nodelist:
            n_2 = second_node + '_NOUN'
            if second_node != first_node:
                sim = model.similarity(n_1, n_2)
                if sim > 0.5:
                    G.add_edge(first_node, second_node, weight=sim)

    nx.write_gexf(G, file)


## Визуализируем граф в matplotlib
def graph_maker(GR):
    pos = nx.spring_layout(GR)
    nx.draw_networkx_nodes(GR, pos, node_color = '#98eff9', node_size = 50)
    nx.draw_networkx_edges(GR, pos, edge_color = '#06470c') 
    nx.draw_networkx_labels(GR, pos, font_size = 15, font_family = 'Georgia')
    plt.axis('off')
    plt.show() ## Сохраняем картинку и закрываем окно с ней, иначе программа не выдаст дальнейшие результаты
    

## Вычисляем 10 центральных слов
def central_words(GR):
    print('Центральные слова графа:')
    degree = nx.degree_centrality(GR)
    i = 0
    for nodeid in sorted(degree, key=degree.get, reverse = True):
        if i <= 10:
            i += 1
            print(nodeid)


## Вычисляем коэффициент кластеризации
def clusterization(GR):
    print('Коэффициент кластеризации графа:')
    print(nx.average_clustering(GR))


## Вычисляем радиусы для каждой компоненты связности    
def radius(GR):
    print('Радиусы компонент связности: ')
    for component in nx.connected_components(GR):
        sub_GR = GR.subgraph(component)
        print(str(component) + ' : ' + str(nx.radius(sub_GR)))
    

def main():
    file = 'supernatural.gexf' ## Название файла, в который сохраняем граф и откуда потом будем его подгружать
    words = ['тварь', 'существо', 'создание', 'черт', 'чертик', 'чертенок', 'Дьявол',
             'дьявол', 'дьяволенок', 'дьяволица', 'демон', 'Сатана', 'ангел', 'серафим',
             'фея', 'эльф', 'гоблин', 'орк', 'гном', 'вампир', 'вурдалак', 'упырь',
             'русалка', 'ведьма', 'колдун', 'водяной', 'кикимора', 'леший', 'Баба Яга',
             'призрак', 'привидение', 'полтергейст', 'бес', 'Бог', 'бог', 'божество',
             'дух', 'Архангел', 'сирена', 'зомби', 'домовой', 'дракон', 'единорог',
             'феникс', 'оборотень', 'монстр', 'нефилим', 'джинн', 'голем', 'тролль',
             'великан', 'циклоп', 'фавн', 'сатир', 'кентавр', 'суккуб', 'ламия'] ## Список наших слов 
    model = model_creator()
    G =  nodes(model, words)
    edges(model, G, file)
    GR = nx.read_gexf(file) ## Во время визуализации графа и его анализа будем читать граф из отдельного файла
    graph_maker(GR)
    central_words(GR)
    clusterization(GR)
    radius(GR)


if __name__ == "__main__":
    main()
