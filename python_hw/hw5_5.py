import random
gender = ''

def participle_m():
    with open('singular_m_1.txt', 'r', encoding = 'utf-8') as f1:
        for line in f1:
            men = line.split()
            man = random.choice(men)
    with open('participle_m.txt', 'r', encoding = 'utf-8') as f2:
        for line in f2:
            part_men = line.split()
            part_men = random.choice(part_men)
    return 'El ' + man + ', ' + part_man + ','

def participle_f():
    with open('singular_f_1.txt', 'r', encoding = 'utf-8') as f3:
        for line in f3:
            women = line.split()
            woman = random.choice(women)
    with open('participle_f.txt', 'r', encoding = 'utf-8') as f4:
        for line in f4:
            part_women = line.split()
            part_woman = random.choice(part_women)
    return 'La ' + woman + ', ' + part_woman + ','

def adverb_phrase():
    with open('adverb.txt', 'r', encoding = 'utf-8') as f5:
        for line in f5:
            adv = line.split()
            adverb = random.choice(adv)
    with open('noun.txt', 'r', encoding = 'utf-8') as f6:
        for line in f6:
            add = line.split()
            addition = random.choice(add)
    return adverb + ' ' + addition    

def exclamation():
    with open('noun_3.txt', 'r', encoding = 'utf-8') as f7:
        for line in f7:
            subj = line.split()
            subject = random.choice(subj)
    with open('adj_2.txt', 'r', encoding = 'utf-8') as f8:
        for lines in f8:
            adj = lines.split()
            adjective = random.choice(adj)
    return '!' + subject + ' ' + adjective + '!'

def make_choice():
    choice = random.choice(['f', 'm'])
    if choice == 'm':
        gender == 'm'
    else:
        gender == 'f'
    return gender

def sentence_1(gender):
    if gender == 'm':
        phrase_1 = participle_m()
    else:
        phrase_1 = participle_f()
    return phrase_1

def participles(gender):
    with open('participle_m.txt', 'r', encoding = 'utf-8') as f2:
        for line in f2:
            part_men = line.split()
            part_men = random.choice(part_men)
    with open('participle_f.txt', 'r', encoding = 'utf-8') as f4:
        for line in f4:
            part_women = line.split()
            part_woman = random.choice(part_women)
    if gender == 'm':
        phrase_0 = 'Es ' + part_man
    else:
        phrase_0 = 'Es ' + part_woman
    return phrase_0

def sentence_2():
    return participles(gender) + ' ' + adverb_phrase() + '.'

print(sentence_1(gender))
print(sentence_2())
print(exclamation()) 
              





        
