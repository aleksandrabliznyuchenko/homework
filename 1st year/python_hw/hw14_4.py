import os
import shutil

letters = {}
i = 0
for root, dirs, files in os.walk('.'):
    for d in dirs:
        if letters.get(d[0]) == None:
            letters[d[0]] = 1
        else:
            letters[d[0]] += 1
            
for value in letters.values():
    value = str(value)
    maximum = max(value)
for key, value in letters.items():
    print(key for maximum in range(value))
