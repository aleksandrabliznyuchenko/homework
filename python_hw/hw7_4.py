riddles = {('чайная'): 'ложка', ('Карнавальная'): 'ночь',('Снежная'): 'королева',('Лебединое'): 'озеро',('Северный'): 'полюс',
           ('алая'): 'роза', ('Балтийское'): 'море'}
pluses = 0
mistakes = 0
print('Отгадайте слово по его описанию: \n')
for key in riddles.keys():
    print(key, '.' * len(key))
    riddles.get(key)
    answer = input('Введите ответ: ')
    for value in riddles.values():
        if answer == riddles[key]:
            print('Правильно! \n')
            pluses += 1
            break
        else:
            print('Неправильный ответ :( \n Правильный ответ: ', riddles[key], '\n')
            mistakes += 1
            break
print('Количество правильных ответов: \n', pluses)
print('Количество неправильных ответов: \n', mistakes)
if pluses == 7 or pluses == 6:
    print('Вы молодец!')
elif mistakes == 7 or mistakes == 6:
    print('Не повезло :(')
else:
    print('Хороший результат.')



