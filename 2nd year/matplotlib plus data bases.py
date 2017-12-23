import random
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt_c
import matplotlib.pyplot as plt_n
import matplotlib.pyplot as plt_p


# достаём данные из исходной базы данных
def getting_data():
    conn = sqlite3.connect(r'C:\Users\AleksandraB\Desktop\Programmin~\hittite.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Wordforms')
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data


# создаём новую базу данных, и складываем данные в таблицу со словами
def inserting_data_words(data):
    conn = sqlite3.connect('new_database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Words (id INTEGER PRIMARY KEY, Lemma TEXT, Wordform TEXT, Glosses TEXT)')
    for element in data:
        lemma = element[0]
        wordform = element[1]
        gloss = element[2]
        c.execute('INSERT INTO Words (Lemma, Wordform, Glosses) VALUES(?, ?, ?)',
              [lemma, wordform, gloss])
    conn.commit()
    conn.close()


# создаём таблицу для глоссов в новой базе данных и кладём туда глоссы из файла    
def inserting_data_glosses():
    conn = sqlite3.connect('new_database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS Glosses (id INTEGER PRIMARY KEY, Name TEXT, Meaning TEXT)')
    with open('glossing.txt', 'r', encoding = 'utf-8') as f:
        for line in f:
            element = line.split(' — ')
            name = element[0]
            meaning = element[1]
            c.execute('INSERT INTO Glosses (Name, Meaning) VALUES (?, ?)',
                      [name, meaning])
    conn.commit()
    conn.close()


# достаём глоссы из ьаблицы со словами, делим их на составляющие и создаём частотный словарь
def counting_glosses(known_glosses):
    conn = sqlite3.connect('new_database.db')
    c = conn.cursor()
    c.execute('SELECT Glosses FROM Words')
    glosses = c.fetchall()
    for gloss in glosses:
        unique_glosses = str(gloss).split('.')
        for unique_gloss in unique_glosses:
            unique_gloss = unique_gloss.replace('(', '')
            unique_gloss = unique_gloss.replace(')', '')
            unique_gloss = unique_gloss.replace(',', '')
            unique_gloss = unique_gloss.replace('\'', '')
            if unique_gloss in known_glosses:
                known_glosses[unique_gloss] += 1
            else:
                known_glosses[unique_gloss] = 1
    conn.commit()
    conn.close()
    return known_glosses


# строим столбчатый график падежей
def making_graphs_case(known_glosses):       
    plt_c.bar('NOM', known_glosses['NOM'], color = 'r')
    plt_c.bar('GEN', known_glosses['GEN'], color = 'g')
    plt_c.bar('DAT', known_glosses['DAT'], color = 'b')
    plt_c.bar('LOC', known_glosses['LOC'], color = 'y')
    plt_c.bar('DAT-LOC', known_glosses['DAT-LOC'], color = 'turquoise')
    plt_c.bar('ACC', known_glosses['ACC'], color = 'gold')
    plt_c.bar('ABL', known_glosses['ABL'], color = 'plum')
    plt_c.title('График распределения падежей')
    plt_c.show()
    #plt_c.savefig('plot_cases_hittite.png')


# строим график распределения по лицу-числу    
def making_graphs_face_number(known_glosses):       
    plt_n.bar('1SG', known_glosses['1SG'], color = '#fcb001')
    plt_n.bar('2SG', known_glosses['2SG'], color = 'gold')
    plt_n.bar('3SG', known_glosses['2SG'], color = '#ff9408')
    plt_n.bar('1PL', known_glosses['1PL'], color = 'm')
    plt_n.bar('3PL', known_glosses['3PL'], color = '#b00149')
    plt_n.title('График распределения показателей лица-числа')
    plt_n.show()
    #plt_n.savefig('plot_face_number_hittite.png')


# строим график присутствующих в базе данных частей речи
def making_graphs_parts_of_speech(known_glosses):
    with open('glossing.txt', 'r', encoding = 'utf-8') as f:
        for line in f:
            gloss = line.split(' — ')
            part_of_speech = gloss[0]
            if part_of_speech in known_glosses:
                plt_p.bar(part_of_speech, known_glosses[part_of_speech], color = '#c79fef')

    plt_p.title('График распределения частей речи')
    plt_p.show()
    #plt.savefig('plot_parts_of_speech_hittite.png')


# сделаем график со всеми глоссами
def making_graphs_all(known_glosses):
    i = 1
    markers = ['o', '*', '8', 'D', '^', 'P']
    for key, value in known_glosses.items():
        plt.scatter(i, value, marker=random.choice(markers), s=100)
        plt.text(i + 0.1, value + 0.1, key)
        i += 1
    plt.title('Все глоссы на одном графике')
    plt.show()
    #plt.savefig('plot_all_glosses_hittite.png')


def main():
    known_glosses = {}
    data = getting_data()
    inserting_data_words(data)
    inserting_data_glosses()
    counting_glosses(known_glosses)
    making_graphs_case(known_glosses)
    making_graphs_face_number(known_glosses)
    making_graphs_parts_of_speech(known_glosses)
    making_graphs_all(known_glosses)


if __name__ == '__main__':
    main()


    
