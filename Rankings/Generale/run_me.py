import pandas as pd
import csv
import os
from functions_general import extract_meet_codes_from_calendar, custom_sort, get_meet_info, get_events_link
from scraping_risultati import results_from_sigma


anno = '2024';      regione = '';       categoria = ''      
mese = '';          tipo = '3'

file_gare = 'Generale/link_gare.csv'
file_risultati = 'Generale/link_risultati_gare1.csv'

################# Codici gare (anno, mese, livello, regione, tipo, categoria) ###################
## Se file_gare è già presente viene solo aggiornato con i nuovi codici gara
## la funzione usata restituisce un DataFrame con 'Data' e 'Codice' delle varie gare

df_REG_gare = extract_meet_codes_from_calendar(anno,mese,'REG',regione,tipo,categoria)
df_COD_gare = extract_meet_codes_from_calendar(anno,mese,'COD',regione,tipo,categoria)
df_gare = pd.concat([df_REG_gare, df_COD_gare], ignore_index=True)
df_gare[['Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']] = ''

if os.path.exists(file_gare):
    
    print('\nE\' stato trovato il file ' + file_gare)
    
    df_gare_old = pd.read_csv(file_gare, sep='\t')
    df_gare_new = df_gare[~df_gare['Codice'].isin(df_gare_old['Codice'])]
    df_gare = pd.concat([df_gare_old, df_gare_new], ignore_index=True)
    
    if len(df_gare_new) > 0:
        print('\nSono stati aggiunti i codici gare:\n')
        for cod in df_gare_new['Codice']: print(cod + '\n')
    else: print('\nNon sono stati aggiunti codici gare\n')
else: print('\nNon ho trovato il file ' + file_gare + '. Lo creo')
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

df_gare = get_meet_info(df_gare, 'date_2')
df_gare.to_csv(file_gare, sep='\t', index=False)

##################################################################################################



################# Otteniamo i link a ogni risultato di ogni disciplina per ogni gara #############
## usiamo come DataFrame ['Codice', 'Versione Sigma', 'Disciplina', 'Nome', 'Link']
## per ora ci occupiamo solo di trovare 'Nome' e 'Link'
print('\nOra lavoro per cercare i link agli eventi di ogni gara')
df_gare = pd.read_csv(file_gare, sep='\t')
df_risultati = get_events_link(df_gare)
df_risultati.to_csv(file_risultati, index=False)

""" # Prendo solo quelli con status ok
df_gare_ok = df_gare[df_gare['status'] == 'ok']
df_risultati = pd.DataFrame(columns=['Codice', 'Versione Sigma', 'Disciplina', 'Nome', 'Link'])
df_risultati['Codice', 'Versione Sigma'] = df_gare_ok['Codice', 'Risultati']
if os.path.exists(file_risultati):
    
    print('\nE\' stato trovato il file ' + file_risultati)
    
    df_risultati_old = pd.read_csv(file_risultati)
    df_risultati_new = df_risultati[~df_risultati['Codice'].isin(df_risultati_old['Codice'])]
    df_risultati = pd.concat([df_risultati_old, df_risultati_new], ignore_index=True)
    
    if len(df_risultati_new) > 0:
        print('\nSono stati aggiunti i codici gare:\n')
        for cod in df_risultati_new['Codice']: print(cod + '\n')
    else: print('\nNon sono stati aggiunti codici gare\n')
else: print('\nNon ho trovato il file ' + file_risultati + '. Lo creo') """


