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
        if col.lower() == 'società' or col.lower() == 'club' or col.lower() == 'società stato estero':
            societa_column = col
            break
    if societa_column is None:
        raise ValueError("Unable to find column for 'Società' or 'CLUB'")
    res_df = res_df[['Atleta', 'Anno', 'Cat.', societa_column, 'Prestazione']]

    # Remove the Q, q from heats, remove useless spaces, reset indices
    res_df['Prestazione'] = res_df['Prestazione'].astype(str).str.replace(r'[a-zA-Z]', '', regex=True) # tolgo cose inutili
    res_df['Prestazione'] = pd.to_numeric(res_df['Prestazione'], errors='coerce') # convert to numeric, errors to NaN
    res_df = res_df.dropna(subset=['Prestazione']) # deletes NaN rows
    res_df = res_df.astype(str)
    res_df  = res_df.applymap(lambda x: x.strip())
    res_df = res_df.reset_index(drop=True)
    
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
 
        societa_column = None
        for col in df.columns:                                           # holy fucking shit imma go crazy 1
            if col.lower() == 'società' or col.lower() == 'club' or col.lower() == 'società stato estero':
                societa_column = col
                break
        if societa_column is None:
            raise ValueError("Unable to find column for 'Società' or 'CLUB'")
        df = df[['Atleta', 'Anno', 'Cat.', societa_column, 'Prestazione']] #prendo solo le colonne che voglio
        df = df[df['Prestazione'] != df['Atleta']]
        df['Prestazione'] = df['Prestazione'].astype(str)
        df = df[df['Prestazione'].str.contains(r'\d')]  # Keep rows with at least one digit
        df['Prestazione'] = df['Prestazione'].str.extract(r'(\d[\d.:]*\d)')
        #df['Prestazione'] = df['Prestazione'].astype(str).str.replace(r'[a-zA-Z()]', '', regex=True) #removes letters from results
        #df = df.dropna(subset=['Prestazione']) # deletes NaN rows
        #df['Prestazione'] = df['Prestazione'].apply(lambda x: ''.join(filter(lambda char: char.isdigit() or char in '.:', str(x))))
        #df = df[df.apply(lambda row: 'Regole di qualificazione' not in str(row.values), axis=1)] #tolgo righe inutili
        #df['Prestazione'] = pd.to_numeric(df['Prestazione'], errors='coerce') # convert to numeric, errors to NaN
        #selected_df = selected_df[selected_df.apply(lambda row: 'DQ: Pett.' not in str(row.values), axis=1)] #tolgo righe inutili
        #selected_df['Prestazione'] = selected_df['Prestazione'].astype(str).str.replace(r'(PB|SB)(?=\s+|$)', '', regex=True) # tolgo cose inutili
        #selected_df['Prestazione'] = selected_df['Prestazione'].astype(str).str.replace(r'[qQ()\s]', '', regex=True) # tolgo cose inutili
        if societa_column.lower() == 'club':
            df = df.rename(columns={societa_column: 'Società'}) # holy fucking shit imma go crazy 2
        selected_dfs.append(df)

    # Unisco tutte le tabelle, le converto in stringhe, rimuovo gli spazi inutili, rimuovo i duplicati
    res_df = pd.concat(selected_dfs)
    res_df = res_df.astype(str)
    res_df  = res_df.applymap(lambda x: x.strip())
    res_df = res_df.drop_duplicates() # QUESTO BUGGA UN PO' LE COSE, 2 PRESTAZIONI UGUALI LO STESSO GIORNO DIVENTANO 1
    res_df = res_df.reset_index(drop=True)
    
    # Aggiungo il link alla gara e riordino
    res_df['Gara'] = url
    res_df = res_df[['Prestazione', 'Atleta', 'Cat.', 'Anno', 'Società', 'Gara']]
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

