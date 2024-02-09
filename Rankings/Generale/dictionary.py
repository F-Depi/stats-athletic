import pandas as pd
import csv

## Dizionario per tradurre i nomi scemi che vengono dati agli eventi (es '60Hs Donne', '60 Hs H84 J/P/S Donne', '60Hs H84-8.50 JUNIORES-PROMESSE-SENIORES FEMMINILI')
## in un nome standard che indetifichi univocamente la disciplina (es '60 Hs h84-8.50')
## Sono sostanzialmente fatti a mano guardando tutti quelli che get_results_links ha trovato nelle gare.

file_key = 'Generale/link_risultati_gare_key.csv'
file_dict = 'Generale/event_dict.csv'
"""df_link_risultati = pd.read_csv(file_key)
discipline = df_link_risultati['Disciplina'].tolist()
nomi = df_link_risultati['Nome'].tolist()

event_dict = {}

for disciplina, nome in zip(discipline, nomi):
    if nome not in event_dict:
        # If the disciplina is not in the dictionary yet, create a new entry
        # with a list containing the current nome
        event_dict[nome] = [disciplina]

        
 for disciplina, nomi in event_dict.items():
    print(f"{disciplina}: {nomi}") 

with open(file_dict, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for disciplina, nomi in event_dict.items():
        writer.writerow([disciplina] + nomi) """

event_dict = {}
with open(file_dict, 'r', newline='') as csv_file: #apro il dizionario
    reader = csv.reader(csv_file)
    for row in reader:
        disciplina = row[0]
        nomi = row[1:]
        event_dict[disciplina] = nomi
if '60 Hs H 106 ASSOLUTI UOMINI' in event_dict:
    print(event_dict['60 Hs H 106 ASSOLUTI UOMINI'])