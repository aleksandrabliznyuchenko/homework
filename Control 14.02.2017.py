import re
with open('island.txt', 'r', encoding = 'utf-8') as f1:
    text = f1.read(). replace(' ', '')
    lines = text.split()
    number = 1
    for line in lines:
        if '/teiHeader' not in line:
            number += 1
        elif '/teiHeader' in line:
            break
with open('number.txt', 'w', encoding = 'utf-8') as f2:
    f2.write(str(number))


with open('island.txt', 'r', encoding = 'utf-8') as f3:
    text = f3.read(). replace(' ', '')
    lines = text.split()
    for line in lines:
        if 'wlemma' in line:
            rline = line.split()
            print(rline)
    
                
            



    
