import pandas as pd
import csv
import os
from Generale.calendario import extract_meet_codes_from_calendar
from functions_general import get_meet_info
from scraping_risultati import results_from_sigma
from manage_file import write_file, read_file



anno = '2024';      regione = '';       categoria = ''      
mese = '';          tipo = '3'

file_gare = 'Generale/link_gare.csv'
file_risultati = 'Generale/link_risultati_gare_key.csv'

################# Codici gare (anno, mese, livello, regione, tipo, categoria) ###################
## Se file_gare è già presente viene solo aggiornato con i nuovi codici gara

codici_regionali = extract_meet_codes_from_calendar(anno,mese,'REG',regione,tipo,categoria)
codici_nazionali = extract_meet_codes_from_calendar(anno,mese,'COD',regione,tipo,categoria)
df_gare = pd.DataFrame(codici_regionali + codici_nazionali, columns=['Codice'])
df_gare[['Home','Risultati','Versione Sigma','Status']] = ''

if os.path.exists(file_gare):
    df_gare_old = pd.read_csv(file_gare, sep='\t')
    df_gare_new = df_gare[~df_gare['Codice'].isin(df_gare_old['Codice'])]
    df_gare = pd.concat([df_gare_old, df_gare_new], ignore_index=True)
    print('\nSono stati aggiunti i df_gare\n')
    print(df_gare_new['Codice'])
    
    #df_gare_new.to_csv(file_gare, mode='a', header=False, sep='\t', index=False)
#################################################################################################



################# Link ai risultati (Codici delle gare, Disciplina scelta)   ####################
## aggiorna il DataFrame delle gare controllando se sono disponibili nuovi link nelle gare
## con status diverso da 'ok'.
## Controlla anche di nuovo tutte le gare con il sigma vecchio, perché in quel caso il numero di
# link potrebbe aumentare
## Il DataFrame deve essere già del tipo ['Home','Risultati','Versione Sigma','Status']
df_gare = get_meet_info(df_gare)
df_gare.to_csv(file_gare, sep='\t', index=False)
##################################################################################################



################# Prendiamo i risultati che ci sono nei link e salviamoli ########################
## Questa è la parte più ostica. Ogni link potrebbe avere typo, colonne con nomi diversi. etc.
## Di solito bisogna runnare il codice più volte e modificare le funzioni in scraping_risultati.py
## in base agli errori che saltano fuori.
""" links = read_file(file_link); l=len(links)
header_written = False # we need to write the header once
for i, link in enumerate(links):
    print('\nLink '+str(i+1)+'/'+str(l)+': '+link)
    data = results_from_sigma(link)
    data['Disciplina'] = Disciplina
    data = data[['Prestazione', 'Atleta', 'Cat.', 'Anno', 'Società', 'Disciplina', 'Gara']]
    mode = 'a' if header_written else 'w'
    data.to_csv(file_results, mode=mode, index=False, header=not header_written)
    header_written = True  # Set to True after writing the header once """
##################################################################################################



################# Prendiamo i dati dal csv e tiriamo fuori i ranking    ##########################
""" data = pd.read_csv(file_results)
    
data = data.sort_values(by='Prestazione') # Sort the DataFrame based on the 'Prestazione' column
data = data.drop_duplicates(subset='Atleta', keep='first') # only keeps the best result for each athlete
data.to_csv(file_rankings, index=False) """



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


