import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.api import DataFrame
import requests
import re
from datetime import date, datetime


def extract_meet_codes_from_calendar(anno, mese, livello, regione, tipo, categoria) -> pd.DataFrame | None:
    ## Scarica informazioni sulle gare presenti nel calendario fidal https://www.fidal.it/calendario.php
     # Per ogni gara scarica codice gara, data, nome, home page della gara
     # 'Ultimo Aggiornamento' è messo di defaul al 31 marzo 1896, data simbolica per dire che i risultati
     # non sono stati aggiornati di recente
     #
     # extract_meet_codes_from_calendar(str, str, str, str, str, str) --> DataFrame
     # Input: fare riferimento a Readme.txt
     # Output è un DataFramne con columns=['Data', 'Codice', 'Ultimo Aggiornamento', 'Nome', 'Home Gara']
    
    ## Componiamo il link con i parametri del filtro
    url = 'https://www.fidal.it/calendario.php?anno='+anno+'&mese='+mese+'&livello='+livello+'&new_regione='+regione+'&new_tipo='+tipo+'&new_categoria='+categoria+'&submit=Invia'
    response = requests.get(url)

    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='table_btm')
        
        dates = []
        meet_code = []
        nome_gara = []
        home_gara = []
        
        if div:
            ## Testo con la data del meeting 
            b_elements = div.find_all('b')

            for b in b_elements:

                if 'title' in b.attrs:
                    meet_date = b.get_text(strip=True) # il format è 31/12, 30-31/12, 31/12-01/01. Quindi mi basta prendere gli ultimi 5 caratteri
                    last_day = int(meet_date[-5:-3])
                    month = int(meet_date[-2:])
                    dates.append(date(int(anno), month, last_day))
            
            ## Link, codice e nome del meeting
            a_elements = div.find_all('a', href=True)

            for a in a_elements:
                href = a['href']
                match = re.search(fr'{livello}(\d+)', href)

                nome_gara.append(a.get_text(strip=True))
                home_gara.append(href)
                meet_code.append(match[0])
                
            df = pd.DataFrame({'Data': dates, 'Codice': meet_code, 'Ultimo Aggiornamento':date(1896, 3, 31), 'Nome': nome_gara, 'Home Gara': home_gara}) # first modern olympics date
            
            return df


        else:
            print('No tables with class \'table_btm\' found')
            return None
        
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return None



def get_meet_info(df_gare, update_criteria) -> pd.DataFrame | None:
    ## Trova i link da mettere nelle colonne 'Home', 'Risultati' per ogni meeting
     # aggiorna anche le colonne 'Versione Sigma','Status','Ultimo Aggiornamento' perché sono utili.
     #
     # Inizia controllando se esiste 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm'
     # e, in caso affermativo, continua cercando la pagina di risultati e la versione di sigma utilizzata
     #
     # get_meet_info(DataFrame, str) --> DataFrame
     # DataFrame in input columns=[Data','Codice','Nome','Home Gara','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']
     # DataFrame in output è la stessa ma aggiornata
     # 'Data' e 'Ultimo Aggiornamento' devono essere riconosciuti da python come date() formato YYYY-MM-DD
     # update_criteria: 'all' per ricontrollare tutte le righe
     #                  'date_N' per aggiornare solo le gare che non sono state aggiornate nell'intorno di N giorni
     #                           dalla data della gara stessa
     #                  'status' aggiorna le gare che hanno status diverso da 'ok' assieme al quelle che hanno
     #                           Sigma Vecchio #1 e #2
    
    ## Uniformiamo il formato delle date
    todayis = datetime.today()#date of today
    df_gare['Ultimo Aggiornamento'] = pd.to_datetime(df_gare['Ultimo Aggiornamento'])
    df_gare['Data'] = pd.to_datetime(df_gare['Data'])

    ## Selezioniamo le righe del DataFrame da aggiornare
    if update_criteria.startswith('date_'):
        time_span = int(update_criteria.split('_')[1]) # days around the meet I'm looking for updates

        print('Aggiorno i link nell\'intorno di ' + str(time_span) + ' giorni.')

        # Rows I want to check: if today is 7 days from/prior to the meet, or if it wasn't updated N days after the meet
        diff_update = (df_gare['Ultimo Aggiornamento'] - df_gare['Data']).dt.days
        diff_today_data = (todayis - df_gare['Data']).dt.days
        date_condition = (abs(diff_today_data) < time_span) | ( (diff_update < time_span) & (diff_today_data > 0) )
        
        indices = df_gare.index[date_condition].tolist()
    
    elif update_criteria == 'status':
        print('Aggiorno i link per le gare con status diverso da \'ok\' e quelle con il Sigma Vecchio #1 e #2.')
        indices = df_gare.index[(df_gare['Status'] != 'ok') | (df_gare['Versione Sigma'] == 'Vecchio #1') | (df_gare['Versione Sigma'] == 'Vecchio #2')].tolist()
    
    elif update_criteria == 'all':
        print('Aggiorno tutte le gare.')
        indices = df_gare.index.tolist()
        
    else:
        print('Update criteria non valido. Quelli validi sono:\n\'date_N\', \'status\' and \'all\'')
        return None
    
    if indices == []:
        print('Non c\'è nulla da aggiornare')
        return df_gare
    
    ## Aggiornamento
    print('Aggiorno i link da '+str(indices[0]+1)+' a '+str(indices[-1]+1)+':\n')
    tot = len(df_gare)

    for ii in indices:
        print('\t' + str(ii+1) + '/' + str(tot), end="\r")
        cod = df_gare.loc[ii, 'Codice']
        
        meet_year = str(df_gare.loc[ii, 'Data'].year) # serve per creare il link
        url3 = 'https://www.fidal.it/risultati/' + meet_year + '/' + cod + '/Index.htm' # link della home
        r3 = requests.get(url3).status_code
        
        if r3 == 404: # la home è comune a tutti, quindi deve esistere se esiste una pagina della gara
            df_gare.loc[ii,'Home'] = ''
            df_gare.loc[ii,'Risultati'] = ''
            df_gare.loc[ii,'Versione Sigma'] = ''
            df_gare.loc[ii,'Status'] = 'Gara non esistente'
            
        elif r3 == 200: # C'è la home. Ora devo solo capire che versione di sigma c'è. Arrivato a questo punto coinsidero possibile solo che le richieste abbiamo come risposta 200 o 404.
            df_gare.loc[ii,'Home'] = url3

            ## Vediamo se è sigma nuovo
            url1 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/Risultati/IndexRisultatiPerGara.html'
            r1 = requests.get(url1).status_code
            if r1 == 200:                                                                               # trovato nuovo con risultati
                df_gare.loc[ii,'Risultati'] = url1
                df_gare.loc[ii,'Versione Sigma'] = 'Nuovo'
                df_gare.loc[ii,'Status'] = 'ok'
                continue
            
            url1_1 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/Iscrizioni/IndexPerGara.html'     # trovato nuovo ma senza risultati
            r1_1 = requests.get(url1_1).status_code
            if r1_1 == 200:
                df_gare.loc[ii,'Risultati'] = ''
                df_gare.loc[ii,'Versione Sigma'] = 'Nuovo'
                df_gare.loc[ii,'Status'] = 'Risultati non ancora disponibili'
                continue
            
            ## Vediamo se è sigma vecchio
            url2 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/RESULTSBYEVENT1.htm'                # trovato vecchio con risultati
            r2 = requests.get(url2).status_code
            if r2 == 200:
                df_gare.loc[ii,'Risultati'] = url2
                df_gare.loc[ii,'Versione Sigma'] = 'Vecchio #1'
                df_gare.loc[ii,'Status'] = 'ok'
                
                # Possono esistere anche /RESULTSBYEVENT2.htm, /RESULTSBYEVENT3.htm, ..., /RESULTSBYEVENTN.htm
                for jj in range(2, 30):
                    
                    url2_jj = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/RESULTSBYEVENT'+str(jj)+'.htm'
                    r2_jj = requests.get(url2_jj).status_code
                    if r2_jj == 200:
                        if jj == 4: print('Attenzione questa gara ha più di 3 link: '+url2_jj)
                        if jj == 21: print('ATTENZIONE questa gara ha più di 20 link: '+url2_jj)
                        df_gare.loc[ii,'Versione Sigma'] = 'Vecchio #'+str(jj)

                    else: continue
                    
                continue
            
            url2_1 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/entrylistbyevent1.htm'            # trovato vecchio senza risultati
            r2_1 = requests.get(url2_1).status_code
            if r2_1 == 200:
                df_gare.loc[ii,'Risultati'] = 'Non ancora disponibili'
                df_gare.loc[ii,'Versione Sigma'] = 'Vecchio'
                df_gare.loc[ii,'Status'] = 'Risultati non ancora disponibili'
                continue

            ## Se non è pan è polenta. Questo deve essere sigma vecchissimo
            df_gare.loc[ii,'Risultati'] = url3
            df_gare.loc[ii,'Versione Sigma'] = 'Vecchissimo'
            df_gare.loc[ii,'Status'] = 'ok'
            
                
        else: print('la risposta della pagina è ' + str(r3) + '... e mo\'?')
    
    df_gare.loc[indices, 'Ultimo Aggiornamento'] = todayis
    
    df_gare['Ultimo Aggiornamento'] = pd.to_datetime(df_gare['Ultimo Aggiornamento']).dt.date
    df_gare['Data'] = pd.to_datetime(df_gare['Data']).dt.date

    return df_gare



def get_events_link(df_gare, update_criteria, *arg):
    ## Cerca i risultati di ogni gara presente nella pagina di risultati del meeting
     # esesmpio pagina del meeting https://www.fidal.it/risultati/2024/REG33841/Risultati/IndexRisultatiPerGara.html
     # Salva anche il nome con cui compare quella disciplina.
     #
     # get_events_link(DataFrame, str, DataFrame) --> DataFrame
     # 1° DataFrame in input con columns=['data','codice','home','risultati','versione sigma','status','ultimo aggiornamento']
     # 2° DataFrame in input è lo stesso di quello in output
     # DataFrame in output columns=['codice','versione sigma','warining','disciplina','nome','link']
     # 'Data' and 'Ultimo Aggiornamento' devono essere riconosciuti come date() da python
     # update_criteria: 'ok' per cotrollare tutte le gare con status 'ok'
     #                  'date_N' per controllare solo le gare svolte da N giorni. In questo caso bisogna anche dare in input il DataFrame da aggiornare
     #                           dopo update_criteria
    

    df_risultati = pd.DataFrame(columns=['Codice', 'Versione Sigma', 'Warning', 'Disciplina', 'Nome', 'Link'])

    ## Uniformiamo il formato delle date
    todayis = datetime.today()#date of today
    df_gare['Ultimo Aggiornamento'] = pd.to_datetime(df_gare['Ultimo Aggiornamento'])
    df_gare['Data'] = pd.to_datetime(df_gare['Data'])
    
    if update_criteria == 'ok':
        print('Aggiorno tutti i link con status = \'ok\'')
        cond_update = (df_gare['Status'] == 'ok')
        
    elif update_criteria.startswith('date_'):
        time_span = int(update_criteria.split('_')[1]) # quanti giorni dopo la gara continuo a cercare risultati
        print('Aggiorno tutti i link delle gare finite da al massimo ' + str(time_span) + ' giorni')
        cond_update = (df_gare['Status'] == 'ok') & ((todayis - df_gare['Data']).dt.days.between(0, time_span))
        df_risultati_old = arg[0]
        
    else:
        print('Update criteria \'' + update_criteria + '\' not valid. Valids one are \'ok\' and \'date_N\' where N is an integer')
        return
    

    data = None
    updated_cods = []
    
    ## Link al sigma NUOVO
    df_links_nuovi = df_gare[(df_gare['Versione Sigma'] == 'Nuovo') & cond_update].reset_index(drop=True)
    tot = str(len(df_links_nuovi))

    if int(tot) == 0:
        print('Non ci sono link al sigma nuovo da aggiornare')

    else:
        print('\nAnalizzo i link al sigma nuovo:\n')

        for ii, row in df_links_nuovi.iterrows():
            print('\t' + str(ii+1) + '/' + tot, end="\r")
            cod = row['Codice']
            updated_cods.append(cod)
            url = row['Risultati']

            r = requests.get(url).text
            soup = BeautifulSoup(r, 'html.parser')
            elements = soup.find_all('a')
            
            for element in elements:
                link = element['href']
                
                if link[0] != '#':
                    nome = element.text.strip()
                    link = url[:-26] + link
                    data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Nuovo', 'Nome':nome, 'Link':link}])
                    df_risultati = pd.concat([df_risultati, data])
            
            if data is None: print('Link vuoto: '+url)

            data = None

    ## Link al sigma VECCHIO 
    df_vecchio = df_gare[df_gare['Versione Sigma'].str.contains('#') & cond_update]
    urls = []
    for ii, row in df_vecchio.iterrows():
        cod = row['Codice']
        link = row['Risultati']

        # Con il sigma vecchio posso avere N pagine di risultati. La cella si chiama quindi 'Sigma Vecchio #N'
        N = int(row['Versione Sigma'].split('#')[1])
        # Creo un link per ognuna di queste pagine
        for jj in range(1, N+1):
                link_jj = link[:-5]+str(jj)+link[-4:]
                urls.append([cod, link_jj])

    tot = str(len(urls))
    if int(tot) == 0:
        print('Non ci sono link al sigma vecchio da aggiornare')

    else:
        print('\nAnalizzo i link al sigma vecchio:\n')

        for ii, row in enumerate(urls):
            cod = row[0]
            url = row[1]

            updated_cods.append(cod)

            print('\t' + str(ii+1) + '/' + tot, end="\r")

            r = requests.get(url).text
            soup = BeautifulSoup(r, 'html.parser')
            elements = soup.find_all('td', id='idx_colonna1')

            for element in elements:
                a_tag = element.find('a')
                if a_tag:
                    link = a_tag['href']
                    link = url[:url.rfind('/')] + '/' + link
                    nome = a_tag.get_text(strip=True)
                    data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Vecchio', 'Nome':nome, 'Link':link}])
                    df_risultati = pd.concat([df_risultati, data])
            
            if data is None: print('Link vuoto: '+url)
            data = None

    ## Link al sigma VECCHISSIMO
    df_links_vecchissimi = df_gare[(df_gare['Versione Sigma'] == 'Vecchissimo') & cond_update].reset_index(drop=True)
    
    tot = str(len(df_links_vecchissimi))
    if int(tot) == 0:
        print('Non ci sono link al sigma vecchissimo da aggiornare')

    else:
        print('\nAnalizzo i link al sigma vecchissimo:\n')
    
        for ii, row in df_links_vecchissimi.iterrows():
            print('\t' + str(ii+1) + '/' + tot, end="\r")
            cod = row['Codice']
            url = row['Risultati']

            updated_cods.append(cod)

            r = requests.get(url).text
            soup = BeautifulSoup(r, 'html.parser')
            elements = soup.find_all('a') # class_='idx_link' non dovrebbe servire
            
            for element in elements:
                link = element['href']
                if link[4] != 'L':      # gli iscritti hanno il link con la L prima del numero
                    link = url[:-9] + link
                    nome = element.text.strip()
                    data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Vecchissimo', 'Nome':nome, 'Link':link}])
                    df_risultati = pd.concat([df_risultati, data])
            
            if data is None: print('Link vuoto: '+url)
            data = None
                

    df_risultati['Disciplina'] = 'boh'
    df_risultati['Warning'] = ''

    if update_criteria == 'ok':
        print('Ho aggiornato ' + str(len(updated_cods)) + ' codici gare')  

    elif update_criteria.startswith('date_'):
        df_risultati_not_so_old = df_risultati_old[~df_risultati_old['Codice'].isin(updated_cods)]
        len1 = str( len(df_risultati_old)-len(df_risultati_not_so_old) )
        len2 = str(len(df_risultati.reset_index(drop=True)))
        print('\nElimino '+len1+' dei risultati vecchi e ne aggiungo '+len2+' più aggiornati (forse).')

        df_risultati = pd.concat([df_risultati_not_so_old, df_risultati])

    df_risultati = df_risultati.reset_index(drop=True)
    return df_risultati



def hard_strip(nome_str):
    ## prende il nome dato a una gara a un meeting di ateltica
     # e fa del suo meglio per togliere tutte le cose inutili
     # cercando di lasciare solo le informazioni importanti
     #
     # hard_strip(str) --> str


    nome_str = nome_str.strip().lower()
    
    starting_trash = ['modello 1','modello','risultati','classifica']
    for word in starting_trash:
        if nome_str.startswith(word): return 'altro'
    
    nome_str = nome_str.replace('(', ' ').replace(')', ' ').replace('-', ' ')
    
    first_trash = ['finale','extra','ad invito','invito','piani','staffetta','staff.',' u14 ',' u15 ',' u16 ',' u17 ',' u18 ',' u19 ',' u19 ',' u20 ',' u23 ']
    for word in first_trash:
        nome_str = nome_str.replace(word, '')
    
    nome_str = nome_str.replace('metri','m').replace('ostacoli','hs')
    
    second_trash = ['salto con l\'','salto in','salto']
    for word in second_trash:
        if nome_str.startswith(word):
            nome_str = nome_str.replace(word, '')
    
    third_trash = [' ','/','bancari','indoor']
    for word in third_trash:
        nome_str = nome_str.replace(word, '')
        
    fourth_trash = ['asta','lungodafermo','lungo','alto','triplo','quadruplo']
    for word in fourth_trash:
        if nome_str.startswith(word):
            nome_str = word
    
    fifth_trash = ['pesokg1','pesokg2','pesokg3','pesokg4','pesokg5','pesokg6','pesokg7.260','pesospkg1','pesospkg2','pesospkg3','pesospkg4','pesospkg5','pesospkg6','pesospkg7.260']
    for word in fifth_trash:
        if nome_str.startswith(word):
            nome_str = word
            
    return nome_str

    
