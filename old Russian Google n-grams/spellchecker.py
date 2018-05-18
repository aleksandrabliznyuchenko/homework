import os
import re
import json
from collections import defaultdict

        
def get_words(number):
    punct = '.,:;?!-_()[]{}«»""\''
    with open(str(number) + 'grams.txt', 'r', encoding = 'utf-8') as file2:
        text = file2.read().replace('\n', ' ')
        words = text.split()
        words = [word.strip(punct) for word in words if word != ' ']
        return words

 
def train(words):
    freq = defaultdict(lambda: 1)
    for word in words:
        freq[word] += 1
    return freq

            
def pre_edit(insert):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    n = len(insert)
    edits_set = set( [insert[0:i]+insert[i+1:] for i in range(n)] +                      # deletion 
                [insert[0:i]+insert[i+1]+insert[i]+insert[i+2:] for i in range(n-1)] +  # transposition 
                [insert[0:i]+c+insert[i+1:] for i in range(n) for c in alphabet] +  # alteration 
                [insert[0:i]+c+insert[i:] for i in range(n+1) for c in alphabet]) # insertion
    return edits_set    


def known_edits(insert, edits_set, freq):
    edits_in_freq = []
    for edit in edits_set:
        if edit in freq.keys():
            edits_in_freq.append(freq[edit])
    return edits_in_freq, edits_set


def known_edits_2(insert, edits_set, freq, edits_in_freq):
    edits2_set = [pre_edit(edit) for edit in edits_set]
    for edit_set in edits2_set:
        for edit in edit_set:
            if edit in freq.keys():
                edits_in_freq.append(freq[edit])
    return edits_in_freq, edits2_set
        

def final_edit_1(edits_set, edits_in_freq, freq):
    for edit in edits_set:
        if edit in freq.keys():
            if freq[edit] == max(edits_in_freq):
                return edit

            
def final_edit_2(edits2_set, edits_in_freq, freq):
    for edits_set in edits2_set:
        for edit in edits_set:
            if freq[edit] == max(edits_in_freq):
                return edit


def cleaner(elems, num):
    if '_' in elems[num]:
        insert = elems[num].split('_')[0]
    else:
        insert = elems[num]
    return insert


def file_reader(folder, number, words, freq):
    for f in os.listdir(folder):
        with open(os.path.join(folder, f), 'r', encoding = 'utf-8') as file:
            for line in file:
                elems = line.split()
                for num in range(int(number)):
                    insert = cleaner(elems, num)
                    if insert.endswith('ъ'):
                        insert = insert.replace('ъ', '')
                    if insert in freq.keys():
                        print('No correction needed --> ' + insert + ' --> ' + f)
                        line = line.replace(cleaner(elems, num), insert)
                        file_writer(number + 'grams_final.txt', line)
                    else:
                        edits_set = pre_edit(insert)
                        edits_in_freq, edits_set = known_edits(insert, edits_set, freq)
                        if len(edits_in_freq) == 0:
                            edits_in_freq, edits2_set = known_edits_2(insert, edits_set, freq, edits_in_freq)
                            print('No suitable edits for ' + insert + ' --> ' + f)
                            line = line.replace(cleaner(elems, num), insert)
                            file_writer(number + 'grams_final.txt', line)
                        else:
                            if edits2_set == True:
                                edit = final_edit_2(edits2_set, edits_in_freq, freq)
                                print(elems[num] + ' transformed into ' + edit + ' --> ' + f)
                                line = line.replace(cleaner(elems, num), edit)
                                file_writer(number + 'grams_final.txt', line)
                            else:
                                edit = final_edit_1(edits_set, edits_in_freq, freq)
                                print(elems[num] + ' transformed into ' + edit + ' --> ' + f)
                                line = line.replace(cleaner(elems, num), edit)
                                file_writer(number + 'grams_final.txt', line)



def file_writer(filename, data):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(data)


def main():
    folder = input('Введите название папки: ')
    number = folder[0]
    words = get_words(number)
    freq = train(words)
    #for num in range(int(number)):
    file_reader(folder, number, words, freq)
 
if __name__ == "__main__":
    main()
