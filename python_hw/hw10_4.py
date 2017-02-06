import re
with open('lomonosov.html', 'r', encoding = 'utf-8') as f1:
    text = f1.read()
    lines = text.split('\n', 20)
    science = lines[19]
with open('science.txt', 'w', encoding = 'utf-8') as f2:
    f2.write(science)
   
    

    
    




