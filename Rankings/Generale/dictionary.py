import pandas as pd
import csv

## Dizionario per tradurre i nomi vari che vengono dati agli eventi (es '60Hs Donne', '60 Hs H84 J/P/S Donne', '60Hs H84-8.50 JUNIORES-PROMESSE-SENIORES FEMMINILI')
## in un nome standard che indetifichi univocamente la disciplina (es '60 Hs h84-8.50')
## Sono sostanzialmente fatti a mano guardando tutti quelli che get_results_links ha trovato nelle gare.

file_dizionario = 'Generale/event_dict.csv'
file_dizionario_new = 'Generale/event_dict_new.csv'
discipline = []
nomi = []
with open(file_dizionario, 'r', newline='') as csv_file: #apro il dizionario
    reader = csv.reader(csv_file)
    for row in reader:
        disciplina = row[1]
        nome = row[0].strip().replace(' ','').lower() # Tolgo subito un po' di cose inutili dai nomi
        discipline.append(disciplina)
        nomi.append(nome)
        
event_dict = {}
for disciplina, nome in zip(discipline, nomi):
    if nome not in event_dict:
        # If the disciplina is not in the dictionary yet, create a new entry
        # with a list containing the current nome
        event_dict[nome] = [disciplina]

"""
for disciplina, nomi in event_dict.items():
    print(f"{disciplina}: {nomi}") 
"""

with open(file_dizionario_new, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for nome, disciplina in event_dict.items():
        writer.writerow([nome] + disciplina)
