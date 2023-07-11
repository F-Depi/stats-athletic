import os
import csv

def min2sec(time):
    if ':' in time:
        minutes, seconds = map(float, time.split(':'))
        return minutes * 60 + seconds
    else:
        return float(time)
    
def raw_sorting(in_folder):

    out_folder = in_folder.replace('raw', 'sorted')
    os.makedirs(out_folder)

    for file_name in os.listdir(in_folder):
        with open(f'{in_folder}/{file_name}','r') as in_f:
            data = list(csv.reader(in_f))
        sorted_data = sorted(data[1:], key=lambda row: min2sec(row[0]))
        sorted_data = [data[0]] + sorted_data
        
        with open(f'{out_folder}/sorted_{file_name}', 'w', newline='') as out_f:
            writer = csv.writer(out_f)
            writer.writerows(sorted_data)