import pandas as pd
import csv
import os
from functions_general import extract_meet_codes_from_calendar, custom_sort, get_meet_info, get_events_link
from scraping_risultati import results_from_sigma
import time
start_time = time.time()


anno = '2024';      regione = '';       categoria = ''      
mese = '';          tipo = '3'

folder = 'indoor_'+anno+'/'
file_gare = folder + 'link_gare.csv'
file_risultati = folder + 'link_risultati.csv'
file_risultati_key = folder + 'link_risultati_key.csv'
file_dizionario = 'Generale/event_dict.csv'

################# Codici gare (anno, mese, livello, regione, tipo, categoria) ###################
## Se file_gare è già presente viene solo aggiornato con i nuovi codici gara
## la funzione usata restituisce un DataFrame con 'Data' e 'Codice' delle varie gare

df_REG_gare = extract_meet_codes_from_calendar(anno,mese,'REG',regione,tipo,categoria)
df_COD_gare = extract_meet_codes_from_calendar(anno,mese,'COD',regione,tipo,categoria)
df_gare = pd.concat([df_REG_gare, df_COD_gare], ignore_index=True)
df_gare[['Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']] = ''

if not os.path.exists(folder): os.makedirs(folder)

if os.path.exists(file_gare):
    
    print('\nE\' stato trovato il file ' + file_gare)
    
    df_gare_old = pd.read_csv(file_gare, sep='\t')
    df_gare_new = df_gare[~df_gare['Codice'].isin(df_gare_old['Codice'])]
    df_gare = pd.concat([df_gare_old, df_gare_new], ignore_index=True)
    
    if len(df_gare_new) > 0:
        print('\nSono stati aggiunti i codici gare:\n')
        for cod in df_gare_new['Codice']: print(cod + '\n')
    else: print('\nNon sono stati aggiunti codici gare\n')
else: print('\nNon ho trovato il file ' + file_gare + '.\nLo creo con i '+str(len(df_gare))+' codici gare trovati.')

## Mettiamo le gare in ordine cronologico
df_gare = df_gare.sort_values(by='Data', key=lambda x: x.apply(custom_sort))
df_gare = df_gare.reset_index(drop=True)

#################################################################################################



################# Link ai risultati (Codici delle gare, Disciplina scelta)   ####################
## In modalità 'date' aggiorna il DataFrame delle gare controllando se sono disponibili nuovi link nelle gare
## che hanno |data_gara - data_oggi| < 7 giorni oppure delle gare passate che hanno
## (data_ultimo_aggiornamento - data_gara) < 7 giorni
## Il DataFrame deve essere già del tipo:
## [Data','Codice','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']

df_gare = get_meet_info(df_gare, 'date_5')
df_gare.to_csv(file_gare, sep='\t', index=False)

##################################################################################################



################# Otteniamo i link a ogni risultato di ogni disciplina per ogni gara #############
## usiamo come DataFrame ['Codice', 'Versione Sigma', 'Disciplina', 'Nome', 'Link']
## per ora ci occupiamo solo di trovare 'Nome' e 'Link'

print('\n\nOra cerco i link agli eventi di ogni gara')
df_risultati = get_events_link(df_gare)
df_risultati.to_csv(file_risultati, index=False)

## Per ora basta così. Lo so. Devo trovare un modo per aggiornare solo i link ai risultati delle
## e non ricercarli tutti ogni volta. Ma è troppo complicato e per ora non riesco a farlo



################# Identifichiamo la disciplina corretta con il dizionari dei nomi #################

df_risultati = pd.read_csv(file_risultati)

print('\nApplico il dizionario per dare il nome corretto agli eventi')
event_dict = {}
with open(file_dizionario, 'r', newline='') as csv_file: #apro il dizionario
    reader = csv.reader(csv_file)
    for row in reader:
        disciplina = row[0]
        nomi = row[1:]
        event_dict[disciplina] = nomi
   
for ii, row in df_risultati.iterrows():
    nome = row['Nome'].strip().replace(' ','').lower()
    if nome in event_dict:
        df_risultati.loc[ii, 'Disciplina'] = event_dict[nome][0]
    else:
        print('\nNon conosco ' + nome)
        event_dict[nome] = ['boh']

df_risultati.to_csv(file_risultati_key, index=False)

with open(file_dizionario, 'w', newline='') as csv_file: # salvo il dizionario con i cambiamenti
    writer = csv.writer(csv_file)
    for disciplina, nome in event_dict.items():
        writer.writerow([disciplina] + nome)
        


print("--- %s secondi ---" % round(time.time() - start_time, 2))