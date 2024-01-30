import pandas as pd
import csv
from calendario import extract_meet_codes_from_calendar
from risultati_gara import extract_link_of_discipline_results
from scraping_risultati import results_from_sigma
from manage_file import write_file, read_file



anno = '2024';      regione = '';       categoria = 'PRO'      
mese = '';          tipo = '3';         Disciplina = '60Hs H106'

file_codici = Disciplina + '/' + 'codici_gare'
file_link = Disciplina + '/' + 'link_2024_01_' + Disciplina
file_resulst = Disciplina + '/' + 'results_2024_01_' + Disciplina + '.csv'

################# Codici gare (anno, mese, livello, regione, tipo, categoria) ###################
## NOTA: per ora extract_link_of_discipline_results() funziona solo per il 2024
## Il calendario fidal non si aggiorna spesso, quindi questa serve una volta al mese circa
""" codici_regionali = extract_meet_codes_from_calendar(anno,mese,'REG',regione,tipo,categoria)
codici_nazionali = extract_meet_codes_from_calendar(anno,mese,'COD',regione,tipo,categoria)
codici = codici_regionali + codici_nazionali
print(codici)
write_file(file_codici, codici) """
##################################################################################################



################# Link ai risultati (Codici delle gare, Disciplina scelta)   ###################
## Da usare se vogliamo i risultati di una disciplina diversa.
## Ottenere i link è lento, quindi conviene salvarli in un file per poi lavorarci meglio.
""" codici = read_file(file_codici)
links = []
for codice in codici:
    link = extract_link_of_discipline_results(codice, Disciplina)
    print(link)
    if link:
        links.extend(link)
write_file(file_link, links) """
##################################################################################################



################# Prendiamo i risultati che ci sono nei link e salviamoli ########################
## Questa è la parte più ostica. Ogni link potrebbe avere typo, colonne con nomi diversi. etc.
## Di solito bisogna runnare il codice più volte e modificare le funzioni in scraping_risultati.py
## in base agli errori che saltano fuori.
""" links = read_file(file_link)
header_written = False # we need to write the header once
for link in links:
    print('\n'+link)
    data = results_from_sigma(link)
    mode = 'a' if header_written else 'w'
    data.to_csv(file_resulst, mode=mode, index=False, header=not header_written)
    header_written = True  # Set to True after writing the header once """
##################################################################################################


""" 
# Otteniamo direttamente la tabellona senza passare per il file (più veloce ma si presta meno al trial and error)
data = []
links = read_file(file_link)
for link in links:
    #print(link)
    data1 = results_from_sigma(link)
    data.append(data1)

data = pd.concat(data).reset_index(drop=True)
print(data)

# Rankings
output_file3 = 'rank__2024_01_60HS_PRO.csv'
data['Prestazione'] = pd.to_numeric(data['Prestazione'], errors='coerce') # Convert 'Prestazione' column to numeric, errors='coerce' will convert non-numeric values to NaN
data = data.dropna(subset=['Prestazione']) # Drop rows with NaN values in the 'Prestazione' column
data = data.sort_values(by='Prestazione') # Sort the DataFrame based on the 'Prestazione' column
data = data.drop_duplicates(subset='Atleta', keep='first') # only keeps the best result for each athlete
data = data.reset_index(drop=True)

data.to_csv(output_file3)   
 """


