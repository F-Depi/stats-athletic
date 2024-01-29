import pandas as pd

def results_OLD_sigma(url):
    dfs = pd.read_html(url)
    dfs = dfs[7:-1]   # the crap before is useless

    # Sort out to only take the tables that contains the heat and not the 'RIEPILOGO', to avoid duplicate results
    riepilogo_index = None

    for i, df in enumerate(dfs):
        if any('RIEPILOGO' in cell for cell in df.values):
            riepilogo_index = i

    if riepilogo_index is not None:
        dfs = [df for i, df in enumerate(dfs) if i not in [riepilogo_index, riepilogo_index+1]]

    # Extract only the tables containing the actual results data. We find them by looking for the word 'Prestazione'
    res_dfs = [df for df in dfs if df.shape[1] > 1 and 'Prestazione' in df.columns]

    # Concatenate the results tables into a single DataFrame
    res_df = pd.concat(res_dfs)

    # Drop rows with NaN values in the "Atleta" column
    res_df = res_df.dropna(subset=['Atleta'])
    
    # Select the desired columns
    res_df = res_df[['Atleta', 'Anno', 'Cat.', 'Società', 'Prestazione']]

    # Remove the Q, q from heats, remove useless spaces, reset indices
    res_df['Prestazione'] = res_df['Prestazione'].astype(str).str.replace(r'[qQ()\s]', '', regex=True) # tolgo cose inutili
    res_df = res_df.astype(str)
    res_df  = res_df.applymap(lambda x: x.strip())    
    res_df = res_df.reset_index(drop=True)
    
    # Add a nice link from to the competition results page
    res_df['Gara'] = url

    return(res_df)


def results_NEW_sigma(url):

    # Carica tutte le tabelle dalla pagina HTML
    dfs = pd.read_html(url)

    selected_dfs = []
    for df in dfs:
            selected_df = df[['Atleta', 'Anno', 'Cat.', 'Società', 'Prestazione']] #prendo solo le colonne che voglio
            selected_df = selected_df[selected_df.apply(lambda row: 'Regole di qualificazione' not in str(row.values), axis=1)] #tolgo righe inutili
            selected_df['Prestazione'] = selected_df['Prestazione'].astype(str).str.replace(r'[qQ()\s]', '', regex=True) # tolgo cose inutili
            selected_dfs.append(selected_df)

    # Unisco tutte le tabelle, le converto in stringhe, rimuovo gli spazi inutili, rimuovo i duplicati
    res_df = pd.concat(selected_dfs)
    res_df = res_df.astype(str)
    res_df  = res_df.applymap(lambda x: x.strip())
    res_df = res_df.drop_duplicates() # QUESTO BUGGA UN PO' LE COSE, 2 PRESTAZIONI UGUALI LO STESSO GIORNO DIVENTANO 1
    res_df = res_df.reset_index(drop=True)
    
    # Aggiungo il link alla gara
    res_df['Gara'] = url

    return(res_df)
    

"""
# Test

url_new = 'https://www.fidal.it/risultati/2024/REG33873/Risultati/Gara420.html#g5'
data_new = results_NEW_sigma(url_new)

url_old = 'https://www.fidal.it/risultati/2024/REG34208/Gara122.htm'
data_old = results_OLD_sigma(url_old)

data = pd.concat([data_new, data_old])

# Save to CSV
data.to_csv('results_old.csv', index=False)
"""


