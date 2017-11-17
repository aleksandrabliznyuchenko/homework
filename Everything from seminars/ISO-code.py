codes = {}

with open ('lang.tsv', 'r', encoding = 'utf-8') as f:
    for lines in f:
        elems = lines.split('\t')
        codes[elems[0]] = elems[1:5]
        for value in codes.values():
            print(value)
