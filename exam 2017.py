import os
import re

def file_opener():
    for roots, dirs, files in os.walk('news'):
        text = ''
        for f in files:
            file_name.append(f)
            with open(os.path.join('news', f), 'r', encoding='Windows-1251') as t:
                text += t.read()
    return text


def word_getter(text):
    word_arr = []
    lines = text.split()
    word_lines = re.findall('(<w>.+</w>)((?:\n?[«»,.! \?\-])*(?:\n?[01234567])*)', text)
    for i in range(len(word_lines)):
        line = word_lines[i][0].strip('<w>').strip('</').split('<ana')
        for e in range(len(line)):
            if e > 0:
                line[e] = line[e].strip(' />')
        word_arr.append([line[0]] + [len(line)-1] + [word_lines[i][1].strip().strip(' ')] + line[1:])
    return word_arr


def counter(word_arr):
    total = 0
    for i in range(len(word_arr)):
        total += word_arr[i][1]
    return total



def main():
    text = file_opener()
    word_arr = word_getter(text)
    print(word_arr)
    average_anas = counter(word_arr)
    print(total)
    


if __name__ == '__main__':
    main()
