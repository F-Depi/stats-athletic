import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def clean_tempo(tempo):
    
    tempo = str(tempo)
    tempo = tempo.upper()
    
    if 'DNF' in tempo: return tempo
    if 'DNS' in tempo: return tempo
    if 'NM' in tempo: return tempo
    if 'DQ' in tempo: return 'DSQ'          # perché sì
    
    IQ_match = re.match(r'(\d[\d.:]*\d)', str(tempo))
    if IQ_match: return IQ_match[0]
    else: return 'boh'


def clean_nome(nome):
    
    nome = nome.replace('(I)','')
    nome = nome.replace('Campionessa Italiana','')
    nome = nome.replace('Campione Italiano','').strip()
    
    return nome


def scrape_nuovo_corse(comptetition_row):
    ## Funzione per fare scraping dei risultati delle corse (individuali), degli ostacoli e della marcia nel sito nuovo ('Versione Sigma' = 'Nuovo')
    ## input è una riga di un DataFrame con columns=['Codice','Versione Sigma','Warning','Disciplina','Nome','Link']
    ## Se la versione del sigma in input non è corretta la funzione stampa un errore e non restituisce nulla
    ## Se la disciplina non è corretta stampa un errore e restituisce un DataFrame vuoto
    ## Restituisce una DataFrame con columns=['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo','Gara]
    
    # Ogni tabella è preceduta da una <div class='row' con alcune informazioni(data, luodo, numero di batteria/finale/serie o se è un riepilogo)
    # devo ancora gestire le start list
    
    # Controllo la versione del sigma
    if comptetition_row['Versione Sigma'] != 'Nuovo':
        print('Versione sigma '+comptetition_row['Versione Sigma']+'. Questa funzione funziona con il sigma nuovo')
        return
    
    url = comptetition_row['Link']
    disciplina = comptetition_row['Disciplina']
    batterie = pd.DataFrame(columns=['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo','Gara'])
    
    # Controllo che sia una corsa individuale o la marcia
    if not(disciplina[0].isdigit() or disciplina.startswith('Marcia')) or 'x' in disciplina:
        print('Non compatibile con '+disciplina+'. Solo corse individuali e marcia.')
        return batterie
    
    # Recupero le linee di testo della pagina (titoli nomi delle batterie per la maggior parte)
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    div_righe = soup.find_all('div', class_='row')

    div_batterie = []
    for a in div_righe[2:]: # le prime 2 div sono di intestazione
        if not(('risultati' in a.text.lower()) or ('results' in a.text.lower()) ): # anche le div con scritto risultati/results sono inutili
            div_batterie.append(a)


    # Ora prendo tutte le tabelle che ci sono
    dfs = pd.read_html(r)
    if dfs[0].iloc[0,0] == 'Record': dfs = dfs[1:]  # a volte la prima tabella ha i record della disciplina
    
    if len(dfs) != len(div_batterie): # controllo se ho filtrato correttamente tabelle e titolo delle tabelle
        print(url)
        print('Ho trovato ' + str(len(div_batterie)) + ' div e ' + str(len(dfs)) + ' tabelle:')
        
    else:
        for a,df in zip(div_batterie, dfs):
            if not(('riepilogo' in a.text.lower()) or ('summary' in a.text.lower())): # la tabella con il riepilogo contiene gli stessi risultati delle altre (se c'è)
                
                if 'Atleta' in df: colonna_atleta = df.columns.get_loc('Atleta')
                elif 'Athlete' in df: colonna_atleta = df.columns.get_loc('Athlete')
                else: print('Non trovo la colonna atleta: ' + url)
                
                batteria_N = df.iloc[:, colonna_atleta:colonna_atleta+5]
                
                while batteria_N.iloc[-1,0] == batteria_N.iloc[-1,1]:   # le ultime righe hanno cose che non sono risultati. Vanno tolte e
                    batteria_N = batteria_N.iloc[:-1,:]                 # sfrutto il fatto che sono la stessa cella ripetutta per tutta la riga
                
                data_batteria = a.find_all('p')[1].text.split('-')[-2].strip()
                luogo_batteria = a.find_all('p')[1].text.split('-')[-3].replace('PHOTOFINISH','').strip()
                
                batteria_N['Data'] = data_batteria
                batteria_N['Luogo'] = luogo_batteria
                batteria_N['Disciplina'] = disciplina
                
                batteria_N = batteria_N.iloc[:, [7, 4, 0, 1, 2, 3, 5, 6]]
                batteria_N.columns = ['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo']
                batteria_N['Gara'] = url
                batteria_N['Prestazione'] = batteria_N['Prestazione'].apply(clean_tempo)

                batterie = pd.concat([batterie, batteria_N]).reset_index(drop=True)
    
    return batterie
            
