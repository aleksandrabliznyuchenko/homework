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
                    
               
