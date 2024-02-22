import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime

def luogo_data_batteria(date_str):
    ## l'input è del tipo 'PHOTOFINISHPalaCasali Ancona - 4 gen 2024 - 11:51'
    ## Gestisce anche cose del tipo 'Raul Guidobaldi - Indoor - 13 gen 2024 - 12:52'
    ## rimuove 'PHOTOFINISH' se c'è
    ## restituisce luogo della batteria e data-ora in formato 'YYYY-MM-DD hh:mm:ss'
    
    match_data = re.search(r'\b\d+ \w+ \d{4}\b', date_str) # 17 gen 2024
    match_ora = re.findall(r'\b\d{2}:\d{2}', date_str)      # 13:57
    
    # Il luogo sembra sempre essere prima della data
    if match_data:
        data_batteria = match_data[0]
        luogo_batteria = date_str.split(data_batteria)[0].replace('PHOTOFINISH','').replace('-','').strip()
    
        mese_batteria = data_batteria.split()[1].lower().strip()[0:3]
        
        mesi = {
        'gen': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'mag': 5, 'giu': 6, 'lug': 7, 'ago': 8,
        'set': 9, 'ott': 10, 'nov': 11, 'dic': 12
        }
    
        parti = data_batteria.split()

        giorno = int(parti[0])
        mese = mesi[mese_batteria]
        anno = int(parti[2])
    
        # A volte manca l'orario, quindi se non c'è mette 00:00:00
        if match_ora:
            ora_batteria = match_ora[-1] # nel sigma vecchio spesso vengono messi l'orario di inizio e poi quello di fine.
            ora, minuti = map(int, ora_batteria.split(':'))
            data_ora = datetime(anno, mese, giorno, ora, minuti)
            
        else:
            data_ora = datetime(anno, mese, giorno)
            
        return luogo_batteria, data_ora
    
    
    # Se non c'è il giorno
    else: return date_str, ''
        
    

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
    nome = nome.replace('(FC)','')
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
                
                (luogo_batteria, data_batteria) = luogo_data_batteria(a.find_all('p')[-1].text)
                
                batteria_N['Data'] = data_batteria
                batteria_N['Luogo'] = luogo_batteria
                batteria_N['Disciplina'] = disciplina
                
                batteria_N = batteria_N.iloc[:, [7, 4, 0, 1, 2, 3, 5, 6]]
                batteria_N.columns = ['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo']
                batteria_N['Gara'] = url
                batteria_N['Prestazione'] = batteria_N['Prestazione'].apply(clean_tempo)
                batteria_N['Atleta'] = batteria_N['Atleta'].apply(clean_nome)

                batterie = pd.concat([batterie, batteria_N]).reset_index(drop=True)
    
    return batterie
            

def scrape_vecchio_corse(competition_row):
    ## Funzione per fare scraping dei risultati delle corse (individuali), degli ostacoli e della marcia nel sito nuovo ('Versione Sigma' = 'Nuovo')
    ## input è una riga di un DataFrame con columns=['Codice','Versione Sigma','Warning','Disciplina','Nome','Link']
    ## Se la versione del sigma in input non è corretta la funzione stampa un errore e non restituisce nulla
    ## Se la disciplina non è corretta stampa un errore e restituisce un DataFrame vuoto
    ## Restituisce una DataFrame con columns=['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo','Gara]
    
    # Controllo la versione del sigma
    if competition_row['Versione Sigma'] != 'Vecchio':
        print('Versione sigma '+competition_row['Versione Sigma']+'. Questa funzione funziona con il sigma nuovo')
        return
    
    url = competition_row['Link']
    disciplina = competition_row['Disciplina']
    batterie = pd.DataFrame(columns=['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo','Gara'])
    
    # Controllo che sia una corsa individuale o la marcia
    if not(disciplina[0].isdigit() or disciplina.startswith('Marcia')) or 'x' in disciplina:
        print('Non compatibile con '+disciplina+'. Solo corse individuali e marcia.')
        return batterie
    
    r = requests.get(url).text
    tabelle = pd.read_html(r)
    tabelle = [tab.astype(str) for tab in tabelle]
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
    
    if len(titoli) != len(tab_risultati): # controllo se ho filtrato correttamente tabelle e titolo delle tabelle
        print(url)
        print('Ho trovato ' + str(len(titoli)) + ' titoli e ' + str(len(tab_risultati)) + ' tabelle:')
        
    else:
        for titolo, a, df in zip(titoli, dataora_tutti, tab_risultati):
            if not('riepilogo' in titolo.text.lower()):
                
                if 'Atleta' in df: colonna_atleta = df.columns.get_loc('Atleta')
                elif 'Athlete' in df: colonna_atleta = df.columns.get_loc('Athlete')
                else: print('Non trovo la colonna atleta: ' + url)
                
                batteria_N = df.iloc[:, colonna_atleta:colonna_atleta+5]
                batteria_N.dropna(inplace=True)
                
                while batteria_N.iloc[-1,0] == batteria_N.iloc[-1,1]:   # le ultime righe hanno cose che non sono risultati. Vanno tolte e
                    batteria_N = batteria_N.iloc[:-1,:]                 # sfrutto il fatto che sono la stessa cella ripetutta per tutta la riga
                
                (luogo_batteria, data_batteria) = luogo_data_batteria(a.text)
                
                batteria_N['Data'] = data_batteria
                batteria_N['Luogo'] = luogo_batteria
                batteria_N['Disciplina'] = disciplina
                
                batteria_N = batteria_N.iloc[:, [7, 4, 0, 1, 2, 3, 5, 6]]
                batteria_N.columns = ['Disciplina', 'Prestazione', 'Atleta','Anno','Categoria','Società','Data','Luogo']
                batteria_N['Gara'] = url
                batteria_N['Prestazione'] = batteria_N['Prestazione'].apply(clean_tempo)
                batteria_N['Atleta'] = batteria_N['Atleta'].apply(clean_nome)
                #batteria_N['Anno'] = batteria_N['Anno'].astype(int)     # non ho idea del perché ma con il sigma vecchio mi trasforma 2002 in 2002.0

                batterie = pd.concat([batterie, batteria_N]).reset_index(drop=True)
                
    return batterie