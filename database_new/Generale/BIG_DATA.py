import pandas as pd
from scrape import scrape_nuovo_corse


df_link = pd.read_csv('database_link/indoor_2023/link_risultati.csv')
df_link = df_link[(df_link['Versione Sigma'] == 'Nuovo')]

write_header = True
for ii,row in df_link.iterrows():
    df_temp = scrape_nuovo_corse(row)
    df_temp.to_csv('TEST2.csv', mode='a', index=False, header=write_header)
    write_header = False