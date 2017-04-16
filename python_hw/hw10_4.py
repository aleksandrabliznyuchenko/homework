import os
import shutil
import re
    
print(os.listdir('.'))
symbols = '[0123456789!+()?><:;\-|/@#$%^&*№="\'~`абвгдеёжзийклмнопрстуфхзчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]'
i = 0
for file in os.listdir('.'):
    m = re.search(symbols, file)
    if m == None:
        i += 1
print(i)
    


    
