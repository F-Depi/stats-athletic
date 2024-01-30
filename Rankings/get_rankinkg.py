import pandas as pd
import csv
from calendario import extract_meet_codes_from_calendar
from risultati_gara import extract_link_of_discipline_results
from scraping_risultati import results_from_sigma

"""

Anno = '2024';      regione = '';       categoria = 'PRO'      
Mese = '';          tipo = '3'


# Codici gare (Anno, Mese, livello, regione, tipo, categoria)
codici_regionali = extract_meet_codes_from_calendar(Anno,Mese,'REG',regione,tipo,categoria)
codici_nazionali = extract_meet_codes_from_calendar(Anno,Mese,'COD',regione,tipo,categoria)
codici = codici_regionali + codici_nazionali


# Link ai risultati (Codici delle gare, Disciplina scelta)
links = []
for codice in codici:
    link = extract_link_of_discipline_results(codice, '60Hs H106')
    if link:
        links.extend(link)


# Visto che recuperare i link è un'operazione relativamente lunga, li scriviamo in un file
with open('link_2024_01_60HS_PRO', 'w') as file1:
    for link in links:
        file1.write(link + '\n')
"""



# Prendiamo i link dal file
links=[]
with open('link_2024_01_60HS_PRO', 'r') as file2:
    for line in file2:
        links.append(line)



"""
# Prendiamo i risultati che ci sono nei link e salviamoli nel file results_2024_01_60HS_PRO.csv

output_file = "results_2024_01_60HS_PRO"
header_written = False # we need to write the header once
for link in links:
    print(link)
    data = results_from_sigma(link)
    mode = 'a' if header_written else 'w'
    data.to_csv(output_file, mode=mode, index=False, header=not header_written)
    header_written = True  # Set to True after writing the header once
"""



# Otteniamo direttamente la tabellona senza passare per il file (più veloce ma si presta meno al trial and error)
data = []
for link in links:
    print(link)
    data1 = results_from_sigma(link)
    data.append(data1)

data = pd.concat(data).reset_index(drop=True)


# Rankings
output_file3 = 'rank__2024_01_60HS_PRO.csv'
data['Prestazione'] = pd.to_numeric(data['Prestazione'], errors='coerce') # Convert 'Prestazione' column to numeric, errors='coerce' will convert non-numeric values to NaN
data = data.dropna(subset=['Prestazione']) # Drop rows with NaN values in the 'Prestazione' column
data = data.sort_values(by='Prestazione') # Sort the DataFrame based on the 'Prestazione' column
data = data.drop_duplicates(subset='Atleta', keep='first') # only keeps the best result for each athlete
data = data.reset_index(drop=True)

data.to_csv(output_file3)
    



