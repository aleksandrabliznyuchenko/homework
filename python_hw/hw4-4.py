word = input('Введите слово: ')
table = []

for i in range (len(word)):
    table.append(word[-i:] + word[:-i])
for elem in table:
    print(elem)
