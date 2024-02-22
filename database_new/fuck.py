import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Generale.scrape import *


file1 = 'database_link/indoor_2024/link_risultati.csv'

df = pd.read_csv(file1)
df = df[df['Versione Sigma'] == 'Vecchio'].reset_index(drop=True)

for ii,row in df.iterrows():
    
    url = row['Link']
    
    r = requests.get(url).text
    tabelle = pd.read_html(r)
    
    # Prendo solo le tabelle con più di 4 colonne. Così sono solo tabelle corrispondenti a risultati(*)
    tab_risultati = []
    for a in tabelle:
        if len(a.columns) >= 5:
            tab_risultati.append(a)

    # (*)il menù di navigazione del sito (HOME Liste x Gara Liste x Team Turni Iniziali Ris. x Gara)
    # è una tabella molto bravo a sembrare una batteria, se c'è lo tolgo
    if 'home' in str(tab_risultati[0].iloc[0,0]).lower():
        tab_risultati = tab_risultati[1:]
    
    # Ora prendo i titoli delle batterie assieme alla riga dove c'è scritto data e ora
    soup = BeautifulSoup(r, 'html.parser')
    titoli = soup.find_all('td', class_='tab_turno_titolo')
    dataora_tutti = soup.find_all('td', class_='tab_turno_dataora')
    
    # Se il titolo è 'riepilogo', allora quella dataora e quella tabella non mi interessano. In questo modo dovrei rimanere solo con batterie/serie/finali
    dataora_batterie = []
    tab_batterie = []
    for titolo, dataora, tab in zip(titoli, dataora_tutti, tab_risultati):
        if not('riepilogo' in titolo.text.lower()):
            dataora_batterie.append(dataora)
            tab_batterie.append(tab)
        
    for a, b in zip(dataora_batterie, tab_batterie):
        print('\n')
        print(a.text)
        print('\n')
        print(b)
    print('-----------------------')
#scrape_vecchio_corse(competition_row)