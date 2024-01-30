import pandas as pd

def results_OLD_sigma(url):
    dfs = pd.read_html(url)
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

    # Remove the empty rows
    res_df = res_df.dropna(subset=['Atleta'])
    
    # Select the desired columns
    societa_column = None
    for col in res_df.columns:                                           # holy fucking shit imma go crazy 1
        if col.lower() == 'società' or col.lower() == 'club' or col.lower() == 'società stato estero': # fare lista in file a parte
            societa_column = col
            break
    if societa_column is None:
        print("Unable to find column for 'Società' in " + url)
        res_df['Società'] = 'Società non trovata'
        societa_column = 'Società'
    
    res_df = res_df[['Atleta', 'Anno', 'Cat.', societa_column, 'Prestazione']]

    # Remove the Q, q from heats, remove useless spaces, reset indices
    df = df.astype(str)
    df = df[df['Prestazione'].str.contains(r'\d')]  # Keep rows with at least one digit
    df['Prestazione'] = df['Prestazione'].str.extract(r'(\d[\d.:]*\d)')
    
    if societa_column.lower() is not None:
        res_df = res_df.rename(columns={societa_column: 'Società'}) # holy fucking shit imma go crazy 2
    
    # Aggiungo il link alla gara e riordino
    res_df['Gara'] = url
    res_df = res_df[['Prestazione', 'Atleta', 'Cat.', 'Anno', 'Società', 'Gara']]
    return(res_df)


def results_NEW_sigma(url):

    # Carica tutte le tabelle dalla pagina HTML
    dfs = pd.read_html(url)
    dfs = [df for df in dfs if df.shape[1] > 1 and 'Prestazione' in df.columns] # prima scrematura
    
    selected_dfs = []
    for df in dfs:
        
        # Prima sistemiamo i problemi con il nome della colonna Società... che è sempre diverso...
        societa_column = None
        for col in df.columns:
            if col.lower() == 'società' or col.lower() == 'club' or col.lower() == 'società stato estero' or col.lower() == 'societa' or col.lower() == 'societa\'':
                df.rename(columns={col: 'Società'}, inplace=True)
                societa_column = 'Found'
                break
        if societa_column is None:
            raise ValueError("Unable to find column Società...")
        
        df = df[['Prestazione', 'Atleta', 'Anno', 'Cat.', 'Società']] #prendo solo le colonne che voglio
        df = df[df['Prestazione'] != df['Atleta']].copy()
        df = df.astype(str)
        df = df[df['Prestazione'].str.contains(r'\d')]  # Keep rows with at least one digit
        df['Prestazione'] = df['Prestazione'].str.extract(r'(\d[\d.:]*\d)')
        
        selected_dfs.append(df)

    # Unisco tutte le tabelle, le converto in stringhe, rimuovo gli spazi inutili, rimuovo i duplicati
    res_df = pd.concat(selected_dfs)
    res_df  = res_df.applymap(lambda x: x.strip())
    res_df = res_df.drop_duplicates() # QUESTO BUGGA UN PO' LE COSE, 2 PRESTAZIONI UGUALI LO STESSO GIORNO DIVENTANO 1
    res_df = res_df.reset_index(drop=True)
    
    # Aggiungo il link alla gara
    res_df['Gara'] = url
    return(res_df)
    


def results_from_sigma(url):
    
    if url[-1] == 'l':
        return(results_NEW_sigma(url))
    elif url[-1] == 'm':
        return(results_OLD_sigma(url))
    else: print('There is something wrong with the link ' + url)
    
    return
    
    
    
    
    
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


