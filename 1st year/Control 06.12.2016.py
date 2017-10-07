with open('Test 1.txt', 'r', encoding = 'utf-8') as f:
    for line in f:
        lines = line.split()
        if len(lines) < 10:
            print(*lines)

quote = 0           
with open('Test 1.txt', 'r', encoding = 'utf-8') as t:
    for line in t:
        lines = line.split()        
        for elem in lines:
            if elem == 'разум':
                quote += 1
    print(quote)
