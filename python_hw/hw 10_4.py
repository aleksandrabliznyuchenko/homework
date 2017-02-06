with open('lomonosov.html', 'r', encoding = 'utf-8') as f1:
    text = f1.read()
    lines = text.split('\n')
    number = 17
    while number != 0:
        line = lines[number]
        if 'Научная' in line:
            sphere = lines[number + 1]
            break
        else:
            number += 1
            continue
    
with open('sphere.txt', 'w', encoding = 'utf-8') as f2:
    f2.write(sphere)
   
    

    
    




