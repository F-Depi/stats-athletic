import pandas as pd
import csv
import os
from Generale.calendario import extract_meet_codes_from_calendar
from functions_general import get_meet_info
from scraping_risultati import results_from_sigma
from manage_file import write_file, read_file



anno = '2024';      regione = '';       categoria = ''      
mese = '3';          tipo = '3'

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
    
#################################################################################################



################# Link ai risultati (Codici delle gare, Disciplina scelta)   ####################
## aggiorna il DataFrame delle gare controllando se sono disponibili nuovi link nelle gare
## con status diverso da 'ok'.
## Controlla anche di nuovo tutte le gare con il sigma vecchio, perché in quel caso il numero di
## link potrebbe aumentare
## Il DataFrame deve essere già del tipo ['Home','Risultati','Versione Sigma','Status']
df_gare = get_meet_info(df_gare)
df_gare.to_csv(file_gare, sep='\t', index=False)
##################################################################################################



################# Otteniamo i link a ogni risultato di ogni disciplina per ogni gara #############



