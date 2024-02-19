import csv

rows = []
with open("database/database_F_I_all/raw_data/1500 metri.csv", 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row.count(':') == 2:
            print("Row contains two colons:", row)