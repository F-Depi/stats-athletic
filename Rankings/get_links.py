from manage_file import read_file, write_file
import pandas as pd
import requests

codici = read_file('Generale/codici_gare')

data_link = pd.DataFrame(index=range(len(codici)), columns=['Codice', 'Home', 'Risultati', 'Versione Sigma'])

for i, cod in enumerate(codici):
    
    data_link.loc[i]['Codice'] = cod
    
    url3 = 'https://www.fidal.it/risultati/2024/' + cod + '/Index.htm' # link della home
    r3 = requests.get(url3).status_code
    
    if r3 == 404: # la home è comune a tutti, quindi deve esistere se esiste una pagina della gara
        data_link.loc[i]['Home'] = ''
        data_link.loc[i]['Risultati'] = 'Gara non esistente'
        data_link.loc[i]['Versione Sigma'] = ''
        
    elif r3 == 200: # C'è la home. Ora devo solo capire che versione di sigma c'è. Arrivato a questo punto coinsidero possibile solo che le richieste abbiamo come risposta 200 o 404.
        data_link.loc[i]['Home'] = url3

        url1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Risultati/IndexRisultatiPerGara.html'
        r1 = requests.get(url1).status_code
        if r1 == 200:                                                                               # trovato nuovo con risultati
            data_link.loc[i]['Risultati'] = url1
            data_link.loc[i]['Versione Sigma'] = 'Nuovo'
            continue
        
        url1_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/Iscrizioni/IndexPerGara.html'     # trovato nuovo ma senza risultati
        r1_1 = requests.get(url1_1).status_code
        if r1_1 == 200:
            data_link.loc[i]['Risultati'] = 'Non ancora disponibili'
            data_link.loc[i]['Versione Sigma'] = 'Nuovo'
            continue
        
        url2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT1.htm'                # trovato vecchio con risultati
        r2 = requests.get(url2).status_code
        if r2 == 200:
            data_link.loc[i]['Risultati'] = url2
            data_link.loc[i]['Versione Sigma'] = 'Vecchio'
            
            # Può esistere anche /RESULTSBYEVENT2.htm
            url2_0_2 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT2.htm'
            r2_0_2 = requests.get(url2_0_2).status_code
            if r2_0_2 == 200:
                data_link.loc[i]['Risultati'] = url2+' '+url2_0_2
                
                # Può esistere anche /RESULTSBYEVENT3.htm
                url2_0_3 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT3.htm'
                r2_0_3 = requests.get(url2_0_3).status_code
                if r2_0_3 == 200:
                    data_link.loc[i]['Risultati'] = url2+' '+url2_0_2+' '+url2_0_3
                    
                    # Non dovrebbe esistere anche /RESULTSBYEVENT4.htm
                    url2_0_4 = 'https://www.fidal.it/risultati/2024/' + cod + '/RESULTSBYEVENT4.htm'
                    r2_0_4 = requests.get(url2_0_4).status_code
                    if r2_0_4 == 200:
                        print('WHAT! Questa pagina ha 4 pagine di risultati: ' + url2_0_4)
            continue
        
        url2_1 = 'https://www.fidal.it/risultati/2024/' + cod + '/ENTRYLISTBYEVENT1.htm'            # trovato vecchio senza risultati
        r2_1 = requests.get(url2_1).status_code
        if r2_1 == 200:
            data_link.loc[i]['Risultati'] = 'Non ancora disponibili'
            data_link.loc[i]['Versione Sigma'] = 'Vecchio'
            continue
        
        data_link.loc[i]['Risultati'] = url3
        data_link.loc[i]['Versione Sigma'] = 'Vecchissimo'
            
    else: print('La risposta della pagina è '+r3+'... e mo\'?')
    
data_link.to_csv('Generale/Link_gara.csv', sep='\t', index=False)

    
    
    
    
    

""" print('Codice numero ' + str(i) + ': ' + cod + '\n')
print('Risposte:')
print('\nNuovo, risultati: ' + str(r1) + '\t\t' + url1)
print('\nNuovo, iscritti: ' + str(r1_1) + '\t\t' + url1_1)
print('\nVecchio, risultati: ' + str(r2) + '\t\t' + url2)
print('\nVecchio, iscritti: ' + str(r2_1) + '\t\t' + url2_1)
print('\nVecchissimo ' + str(r3) + '\t\t\t' + url3)
print('\n -- --------------------------- \n')"""

# Da quello che si capisce da questi risultati la pagina risponde con 404 se non esiste.
# L'importante è testare il link al sigma vecchissimo per ultimo perché /Index.htm per
# qualche motivo corrisponde anche alla home del sistema nuovo e vecchio.
# Quindi, se la gara è nel sistema nuovo ma non ha ancora la pagina dei risultati la richiesta
# a '/Risultati/IndexRisultatiPerGara.html' darà errore, ma quella a '/Index.htm' no...
# devo trovare un modo per capire quando la richiesta a '/Index.htm' è andata a buon
# fine perché la gara è nel sistema vecchio e quando perchè la gara ha solo la home 
# del sistema nuovo
    