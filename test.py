import csv
with open('2325.5.xls', encoding='windows-1251') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        print(row)