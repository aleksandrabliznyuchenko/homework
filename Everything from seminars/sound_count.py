import matplotlib.pyplot as plt
import csv

village_data = {}
formants = []

with open('data-village.csv', 'r', encoding = 'utf-8') as f:
    filereader = csv.reader(f, delimiter=';', quotechar='|')
    for row in filereader:
        village = row[2] + ' - ' + row[3]
        if village in village_data:
            formants.append(row[4])
            formants.append(row[5])
        else:
            village_data[village] = formants
            formants.append(row[4])
            formants.append(row[5])
    print(village_data['Naikhin - i'])
    

           
