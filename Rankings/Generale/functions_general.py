from manage_file import read_file
import pandas as pd
import requests


## Function used by run_me.py to scrape the results meets


def get_meet_info(df_gare):
    ## This function takes a pandas DataFrame with columns=['Codice', 'Home', 'Risultati', 'Versione Sigma', 'Status']
    ## and for each meet code that doesn't have an 'ok' status looks for the existance of the home link
    ## 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm' and, if it exists, goes on looking for the result
    ## page and the version of sigma used at that competition
    ## For stupid reasons it also recheck all the link of sigma vecchio
    
    df_gare = df_gare.loc[(df_gare['Codice'] != df_gare['Codice'].shift(-1)) | (df_gare.index == len(df_gare) - 1)]
    df_gare = df_gare.reset_index(drop=True)

    indices = df_gare.index[(df_gare['Status'] != 'ok') | (df_gare['Versione Sigma'] == 'Vecchio')].tolist()
    kk = 0
    
    for ii in indices:
        
        ii = ii + kk # righe aggiunte
        cod = df_gare.loc[ii, 'Codice']
        
        url3 = 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm' # link della home
        r3 = requests.get(url3).status_code
        
        if r3 == 404: # la home è comune a tutti, quindi deve esistere se esiste una pagina della gara
            df_gare.loc[ii,'Home'] = ''
            df_gare.loc[ii,'Risultati'] = ''
            df_gare.loc[ii,'Versione Sigma'] = ''
            df_gare.loc[ii,'Status'] = 'Gara non esistente'
            
        elif r3 == 200: # C'è la home. Ora devo solo capire che versione di sigma c'è. Arrivato a questo punto coinsidero possibile solo che le richieste abbiamo come risposta 200 o 404.
            df_gare.loc[ii,'Home'] = url3

            url1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Risultati/IndexRisultatiPerGara.html'
            r1 = requests.get(url1).status_code
            if r1 == 200:                                                                               # trovato nuovo con risultati
                df_gare.loc[ii,'Risultati'] = url1
                df_gare.loc[ii,'Versione Sigma'] = 'Nuovo'
                df_gare.loc[ii,'Status'] = 'ok'
                continue
            
            url1_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Iscrizioni/IndexPerGara.html'     # trovato nuovo ma senza risultati
            r1_1 = requests.get(url1_1).status_code
            if r1_1 == 200:
                df_gare.loc[ii,'Risultati'] = ''
                df_gare.loc[ii,'Versione Sigma'] = 'Nuovo'
                df_gare.loc[ii,'Status'] = 'Risultati non ancora disponibili'
                continue
            
            url2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT1.htm'                # trovato vecchio con risultati
            r2 = requests.get(url2).status_code
            if r2 == 200:
                df_gare.loc[ii,'Risultati'] = url2
                df_gare.loc[ii,'Versione Sigma'] = 'Vecchio'
                df_gare.loc[ii,'Status'] = 'ok'
                
                # Può esistere anche /RESULTSBYEVENT2.htm
                url2_0_2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT2.htm'
                r2_0_2 = requests.get(url2_0_2).status_code
                if r2_0_2 == 200:
                    
                    new_row = pd.DataFrame({'Codice': [cod], 'Home': [url3], 'Risultati': [url2_0_2],'Versione Sigma': ['Vecchio'], 'Status': ['ok']})
                    df_gare = pd.concat([df_gare.loc[:ii], new_row, df_gare.loc[ii+1:]], ignore_index=True)
                    
                    kk = kk + 1 # shifto tutti gli indici perché aggiungerò una riga
                    ii = ii + 1
                    print(ii)
                    
                    # Può esistere anche /RESULTSBYEVENT3.htm
                    url2_0_3 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT3.htm'
                    r2_0_3 = requests.get(url2_0_3).status_code
                    if r2_0_3 == 200:
                        
                        kk = kk + 1 # shifto tutti gli indici perché aggiungerò una riga
                        
                        new_row = pd.DataFrame({'Codice': [cod], 'Home': [url3], 'Risultati': [url2_0_3], 'Versione Sigma': ['Vecchio'], 'Status': ['ok']})
                        df_gare = pd.concat([df_gare.loc[:ii], new_row, df_gare.loc[ii+1:]], ignore_index=True)
                        print(ii)                        
                        
                        # Non dovrebbe esistere anche /RESULTSBYEVENT4.htm
                        url2_0_4 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT4.htm'
                        r2_0_4 = requests.get(url2_0_4).status_code
                        if r2_0_4 == 200:
                            print('WHAT! Questa pagina ha 4 pagine di risultati: ' + url2_0_4)
                continue
            
            url2_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/ENTRYLISTBYEVENT1.htm'            # trovato vecchio senza risultati
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
        
    return(df_gare)

