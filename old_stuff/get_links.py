from old_stuff.manage_file import read_file
import pandas as pd
import requests

# MEMO: da qui devi ottenere una funzione che prende il file codici_gare e il file link_gara.csv e aggiunge i codici nuovi ai link e tenta di trovare i link che ancora non ci sono

file_codici = 'Generale/codici_gare'
file_link = 'Generale/link_gare.csv'

codici = read_file(file_codici)

df_links = pd.DataFrame(columns=['Codice', 'Home', 'Risultati', 'Versione Sigma','Status'])
temp_df = pd.DataFrame(index=[0], columns=['Codice', 'Home', 'Risultati', 'Versione Sigma', 'Status'])

for cod in codici:
    
    temp_df['Codice'] = cod
    
    url3 = 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm' # link della home
    r3 = requests.get(url3).status_code
    
    if r3 == 404: # la home è comune a tutti, quindi deve esistere se esiste una pagina della gara
        temp_df['Home'] = ''
        temp_df['Risultati'] = ''
        temp_df['Versione Sigma'] = ''
        temp_df['Status'] = 'Gara non esistente'
        df_links = pd.concat([df_links, temp_df])
        
    elif r3 == 200: # C'è la home. Ora devo solo capire che versione di sigma c'è. Arrivato a questo punto coinsidero possibile solo che le richieste abbiamo come risposta 200 o 404.
        temp_df['Home'] = url3

        url1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Risultati/IndexRisultatiPerGara.html'
        r1 = requests.get(url1).status_code
        if r1 == 200:                                                                               # trovato nuovo con risultati
            temp_df['Risultati'] = url1
            temp_df['Versione Sigma'] = 'Nuovo'
            temp_df['Status'] = 'ok'
            df_links = pd.concat([df_links, temp_df])
            continue
        
        url1_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Iscrizioni/IndexPerGara.html'     # trovato nuovo ma senza risultati
        r1_1 = requests.get(url1_1).status_code
        if r1_1 == 200:
            temp_df['Risultati'] = ''
            temp_df['Versione Sigma'] = 'Nuovo'
            temp_df['Status'] = 'Risultati non ancora disponibili'
            df_links = pd.concat([df_links, temp_df])
            continue
        
        url2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT1.htm'                # trovato vecchio con risultati
        r2 = requests.get(url2).status_code
        if r2 == 200:
            temp_df['Risultati'] = url2
            temp_df['Versione Sigma'] = 'Vecchio'
            temp_df['Status'] = 'ok'
            df_links = pd.concat([df_links, temp_df])
            
            # Può esistere anche /RESULTSBYEVENT2.htm
            url2_0_2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT2.htm'
            r2_0_2 = requests.get(url2_0_2).status_code
            if r2_0_2 == 200:
                print('+')
                temp_df['Codice'] = cod
                temp_df['Home'] = url3
                temp_df['Risultati'] = url2_0_2
                temp_df['Status'] = 'ok'
                df_links = pd.concat([df_links, temp_df])
                
                # Può esistere anche /RESULTSBYEVENT3.htm
                url2_0_3 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT3.htm'
                r2_0_3 = requests.get(url2_0_3).status_code
                if r2_0_3 == 200:
                    print('+')
                    temp_df['Codice'] = cod
                    temp_df['Home'] = url3
                    temp_df['Risultati'] = url2_0_3
                    temp_df['Status'] = 'ok'
                    df_links = pd.concat([df_links, temp_df])
                    
                    
                    # Non dovrebbe esistere anche /RESULTSBYEVENT4.htm
                    url2_0_4 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT4.htm'
                    r2_0_4 = requests.get(url2_0_4).status_code
                    if r2_0_4 == 200:
                        print('WHAT! Questa pagina ha 4 pagine di risultati: ' + url2_0_4)
            continue
        
        url2_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/ENTRYLISTBYEVENT1.htm'            # trovato vecchio senza risultati
        r2_1 = requests.get(url2_1).status_code
        if r2_1 == 200:
            temp_df['Risultati'] = 'Non ancora disponibili'
            temp_df['Versione Sigma'] = 'Vecchio'
            temp_df['Status'] = 'Risultati non ancora disponibili'
            df_links = pd.concat([df_links, temp_df])
            continue
        
        temp_df['Risultati'] = url3
        temp_df['Versione Sigma'] = 'Vecchissimo'
        temp_df['Status'] = 'ok'
        df_links = pd.concat([df_links, temp_df])
        
            
    else: print('La risposta della pagina è '+r3+'... e mo\'?')
    
df_links.to_csv(file_link, sep='\t', index=False)

    
    
    
    
    

""" print('Codice numero ' + str(i) + ': ' + cod + '\n')
print('Risposte:')
print('\nNuovo, risultati: ' + str(r1) + '\t\t' + url1)
print('\nNuovo, iscritti: ' + str(r1_1) + '\t\t' + url1_1)
print('\nVecchio, risultati: ' + str(r2) + '\t\t' + url2)
print('\nVecchio, iscritti: ' + str(r2_1) + '\t\t' + url2_1)
print('\nVecchissimo ' + str(r3) + '\t\t\t' + url3)
print('\n -- --------------------------- \n')"""

# Da quello che si capisce da questi risultati la pagina risponde con 404 se non esiste.
# L'importante è testare il link al sigma vecchissimo per ultimo perché /Index.htm
# anche alla home del sistema nuovo e vecchio.
# Quindi, se la gara è nel sistema nuovo ma non ha ancora la pagina dei risultati la richiesta
# a '/Risultati/IndexRisultatiPerGara.html' darà errore, ma quella a '/Index.htm' no...
# Per capire in che sistema sono se la richiesta a '/Index.htm' da 200 e quella alla pagina dei
# risultati da 404 provo a fare una richiesta alla pagina degli iscritti, che è diversa per ogni
# sistema e c'è sempre, che io sappia.
    