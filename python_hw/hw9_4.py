import re
with open('karenina.txt', 'r', encoding = 'utf-8') as f:
    text = f.read().replace('\n', ' ').lower() 
    words = text.split()
    punct = '.,!?:;-_()""\''
    words = [word.strip(punct) for word in words
             if word != ' ']
    forms = []
    for elem in words:
        m = re.search('(вып(ь(ю(т?)|е(т(е?)м|шь))|и(в(ш?и?й?)|'
                      'т(ь?|ы?(й?|е?|х?|м?и?)|а?я?|о?(г?о?|й?|м?у?)|у?ю?)|л(а?|и?|о?))|ей(т?е?)))', elem)
        if m != None:
            if elem not in forms:
                forms.append(elem)
    for elem in forms:
        print(elem)



