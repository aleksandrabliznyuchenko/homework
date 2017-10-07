quantity = 0
words = 0

with open('Hw5.txt', 'r', encoding ='utf-8') as f:
    for line in f:
        row = line.split()
        for elem in row:
            if elem != ' ':
                words += 1
        for i in elem:
            if i == '.' or ',':
                quantity += 1

print(quantity * 100//words)
# Сейчас программа считает процент слов, оканчивающихся знаком препинания. Для правильного результата:
# sign = quantity * 100//words
# result = 100 - int(sign)
# print(result)
# Но это дошло до меня уже после дедлайна
               
