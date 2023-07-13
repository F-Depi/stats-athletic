# Aiming at creating the top lists (aka list with the best performance for each athlete)

import csv
import os
from scarp_func import min2sec
def top_list(in_folder):

    out_folder = in_folder.replace('raw_data', 'top_lists')
    os.makedirs(out_folder, exist_ok=True)

    for file_name in os.listdir(in_folder):
        with open(f'{in_folder}/{file_name}','r') as in_f:
            data = list(csv.reader(in_f))

        # let's order the result by name of the athlete and then by the result
        rev_order = False
        concorsi = ["Salto", "Peso", "Disco", "Giavellotto", "Martello", "\'", "PENTATHLON", "EPTATHLON", "OCTATHLON", "DECATHLON"]
        if any(concorso in file_name for concorso in concorsi):
            rev_order = True
        sorted_data = sorted(data[1:], key=lambda row: (row[2], -min2sec(row[0])) if rev_order else (row[2], min2sec(row[0])))
        
        # now that we have a blocky list, we keep the first result only
        kk = 0
        best = [sorted_data[0]]
        for row in sorted_data:
            if row[2] != best[kk][2]:
                best.append(row)
                kk += 1
        
        # finally we order everithing again, by the result this time
        sorted_best = sorted(best, key=lambda row: min2sec(row[0]), reverse=rev_order)
        sorted_data = [data[0]] + sorted_best

        with open(f'{out_folder}/list_{file_name}', 'w', newline='') as out_f:
            writer = csv.writer(out_f)
            writer.writerows(sorted_data)


for a in ["M", "F"]:
    for b in ["I", "P"]:
        top_list("database_ANA/assoluti/database_"+a+"_"+b+"_bl012/raw_data")