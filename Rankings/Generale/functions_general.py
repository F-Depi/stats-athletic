from manage_file import read_file
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from datetime import date, datetime

## Function used by run_me.py to scrape the results meets

def extract_meet_codes_from_calendar(anno, mese, livello, regione, tipo, categoria):
    
    # Componiamo il link con i parametri del filtro
    url = 'https://www.fidal.it/calendario.php?anno='+anno+'&mese='+mese+'&livello='+livello+'&new_regione='+regione+'&new_tipo='+tipo+'&new_categoria='+categoria+'&submit=Invia'
    response = requests.get(url)
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='table_btm')
        
        dates = []
        meet_code = []
        
        # These have text with the date of the meet
        b_elements = div.find_all('b')
        for b in b_elements:
            if 'title' in b.attrs:
                meet_date = b.get_text(strip=True) ## il format è 31/12 oppure 30-31/12 oppure 31/12-01/01. Quindi mi basta prendere gli ultimi 5 caratteri
                last_day = int(meet_date[-5:-3])
                month = int(meet_date[-2:])
                dates.append(date(int(anno), month, last_day))
        
        # These have the link with the meet code
        a_elements = div.find_all('a', href=True)
        for a in a_elements:
            href = a['href']
            match = re.search(fr'{livello}(\d+)', href)
            if match:
                meet_code.append(match.group(0))
            
        df = pd.DataFrame({'Data': dates, 'Codice': meet_code, 'Ultimo Aggiornamento':date(1896, 3, 31)}) # first modern olympics date
        
        return df
    
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return []



def get_meet_info(df_gare, update_criteria):
    ## This function takes a pandas DataFrame with
    ## columns=[Data','Codice','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']
    ## and updates the links based on the selected criteria
    ## Starts checking the response of 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm'
    ## and, if it exists, goes on looking for the resultspage and the version of sigma used at that
    ## competition
    ## update_criteria: 'all' to check updates for every meet code
    ##                  'date_N' to check update N days before/after the meet date
    ##                  'status' to check updates for row with non 'ok' status and not al 3 pages of sigma vechio
    
    
    today = datetime.today().date() #date of today
    
    if update_criteria.startswith('date_'):

        time_span = int(update_criteria[-1]) # days around the meet I'm looking for updates
        
        # Rows I want to check: if today is 7 days from/prior to the meet, or if it wasn't updated 7 days after the meet
        diff_update = (df_gare['Ultimo Aggiornamento'] - df_gare['Data']).dt.days
        diff_today_data = (today - df_gare['Data']).dt.days
        date_contition = (abs(diff_today_data) < time_span) | ( (diff_update < time_span) & (diff_today_data > 0) )
        
        indices = df_gare.index[date_contition].tolist()
    
    elif update_criteria == 'status':
        
        # used to remove duplicates rows from sigma vecchio. Not using multiple rows for it as of now
        #df_gare = df_gare.loc[(df_gare['Codice'] != df_gare['Codice'].shift(-1)) | (df_gare.index == len(df_gare) - 1)]
        #df_gare = df_gare.reset_index(drop=True)

        indices = df_gare.index[(df_gare['Status'] != 'ok') | (df_gare['Versione Sigma'] == 'Vecchio #1') | (df_gare['Versione Sigma'] == 'Vecchio #2')].tolist()
    
    elif update_criteria == 'all':
        
        # same here. Only one row for each meet code now.
        #df_gare = df_gare.loc[(df_gare['Codice'] != df_gare['Codice'].shift(-1)) | (df_gare.index == len(df_gare) - 1)]
        #df_gare = df_gare.reset_index(drop=True)
        indices = df_gare.index.tolist()

        
    else: print('Update criteria not valid. Valid update criteria are:\n\'date_N\', \'status\' and \'all\'');
    
    #kk = 0
    if indices == []:
        print('Non c\'è nulla da aggiornare')
        return df_gare
    
    print('Aggiorno i link da '+str(indices[0]+1)+' a '+str(indices[-1]+1)+':\n')
    tot = len(df_gare)
    for ii in indices:
        
        print('\t' + str(ii+1) + '/' + str(tot), end="\r")
        #ii = ii + kk # righe aggiunte
        cod = df_gare.loc[ii, 'Codice']
        
        meet_year = str(df_gare.loc[ii, 'Data'].year)
        url3 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/Index.htm' # link della home
        r3 = requests.get(url3).status_code
        
        if r3 == 404: # la home è comune a tutti, quindi deve esistere se esiste una pagina della gara
            df_gare.loc[ii,'Home'] = ''
            df_gare.loc[ii,'Risultati'] = ''
            df_gare.loc[ii,'Versione Sigma'] = ''
            df_gare.loc[ii,'Status'] = 'Gara non esistente'
            
        elif r3 == 200: # C'è la home. Ora devo solo capire che versione di sigma c'è. Arrivato a questo punto coinsidero possibile solo che le richieste abbiamo come risposta 200 o 404.
            df_gare.loc[ii,'Home'] = url3

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
                        if jj == 4: print('Attenzione questa gara ha più di 3 link:'+url2_jj)
                        if jj == 21: print('ATTENZIONE questa gara ha più di 20 link:'+url2_jj)
                        df_gare.loc[ii,'Versione Sigma'] = 'Vecchio #'+str(jj)
                    else: continue
                    
                continue
            
            url2_1 = 'https://www.fidal.it/risultati/'+meet_year+'/' + cod + '/ENTRYLISTBYEVENT1.htm'            # trovato vecchio senza risultati
            r2_1 = requests.get(url2_1).status_code
            if r2_1 == 200:
                df_gare.loc[ii,'Risultati'] = 'Non ancora disponibili'
                df_gare.loc[ii,'Versione Sigma'] = 'Vecchio'
                df_gare.loc[ii,'Status'] = 'Risultati non ancora disponibili'
                continue
            
            df_gare.loc[ii,'Risultati'] = url3
            df_gare.loc[ii,'Versione Sigma'] = 'Vecchissimo'
            df_gare.loc[ii,'Status'] = 'ok'
            
                
        else: print('La risposta della pagina è '+r3+'... e mo\'?')
    
    df_gare.loc[indices, 'Ultimo Aggiornamento'] = today
    return(df_gare)


def get_events_link(df_gare):
    # the input must be a DataFrame with columns=['Data','Codice','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']
    df_risultati = pd.DataFrame(columns=['Codice', 'Versione Sigma', 'Disciplina', 'Nome', 'Link'])
    df_risultati['Disciplina'] = ''
    
    cond_ok = (df_gare['Status'] == 'ok')
    
    # Link al sigma NUOVO
    print('\nAnalizzo i link al sigma nuovo:\n')
    df_links_nuovi = df_gare[(df_gare['Versione Sigma'] == 'Nuovo') & cond_ok].reset_index(drop=True)
    tot = str(len(df_links_nuovi))
    
    for ii, row in df_links_nuovi.iterrows():
        print('\t' + str(ii+1) + '/' + tot, end="\r")
        cod = row['Codice']
        url = row['Risultati']
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        elements = soup.find_all('div', class_='col-md-6')  # classe della div dove ci sono i link ai risultati
        
        for element in elements:
            anchor = element.find('a')
            
            if anchor:  # non ho idea di cosa sia anchor, ma a quanto pare ogni tanto è vuoto
                link = anchor['href']
                link = url[:-26] + link
                text = anchor.text.strip()
                data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Nuovo', 'Nome':text, 'Link':link}])
                df_risultati = pd.concat([df_risultati, data])
                #df_links_results = df_links_results.append(, ignore_index=True)

    # Link al sigma VECCHIO #1, VECCHIO #2, VECCHIO #3 (ovvero con 1, 2 o 3 link risultati)
    print('\n\nAnalizzo i link al sigma vecchio:\n')
    df_vecchio = df_gare[df_gare['Versione Sigma'].str.contains('#') & cond_ok]
    urls = []
    for i, row in df_vecchio.iterrows():
        cod = row['Codice']
        link = row['Risultati']
        urls.append([cod, link])
        deg = int(row['Versione Sigma'].split('#')[1])
        for jj in range(1, deg):
                link = link[:-5]+str(jj)+link[-4:]
                urls.append([cod, link])

    tot = str(len(urls))
    for ii, row in enumerate(urls):
        cod = row[0]
        url = row[1]
        
        print('\t' + str(ii+1) + '/' + tot, end="\r")
        
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        elements = soup.find_all('td', id='idx_colonna1')

        for element in elements:
            a_tag = element.find('a')
            if a_tag:
                link = a_tag['href']
                link = url[:-19] + link
                text = a_tag.get_text(strip=True)
                data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Vecchio', 'Nome':text, 'Link':link}])
                df_risultati = pd.concat([df_risultati, data])


    # Link al sigma VECCHISSIMO
    print('\n\nAnalizzo i link al sigma vecchissimo:\n')

    df_links_vecchissimi = df_gare[(df_gare['Versione Sigma'] == 'Vecchissimo') & cond_ok].reset_index(drop=True)
    tot = str(len(df_links_vecchissimi))
    for ii, row in df_links_vecchissimi.iterrows():
        print('\t' + str(ii+1) + '/' + tot, end="\r")
        cod = row['Codice']
        url = row['Risultati']

        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        elements = soup.find_all('td', id='idx_colonna2')
        
        for element in elements:
            a_tag = element.find('a')
            if a_tag:
                link = a_tag['href']
                link = url[:-9] + link
                text = a_tag.get_text(strip=True)
                data = pd.DataFrame([{'Codice':cod, 'Versione Sigma':'Vecchissimo', 'Nome':text, 'Link':link}])
                df_risultati = pd.concat([df_risultati, data])
    
    print('\n')
    
    return df_risultati