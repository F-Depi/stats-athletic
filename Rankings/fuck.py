import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

data = pd.read_csv('Generale/link_risultati_gare_key.csv')

data = data[data['Versione Sigma'] == 'Vecchio']
for url in data.loc[:10]['Link']:
    
    print(url)

    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    element = soup.find_all('td', class_='tab_turno_dataora')
    for el in element:
        print(el)
        test = el.get_text(strip=True)
        luogo = test.split('-')[0]
        data = test.split('-')[1].lower()
        data = data.split('ora')[0].strip()
        print(luogo)
        print(data)
        print(test)
    print('------------------')





































""" response = requests.get(url).text

 if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    risultati_table = None
    for table in soup.find_all('table'):
        if 'Risultati' in table.get_text():
            risultati_table = table
            break

    if risultati_table:
        print(risultati_table)
    else:
        print("No table containing 'Risultati' found.")
else:
    print("Failed to retrieve the webpage.") 

   
disciplina = 'alt oUOMINI'

soup = BeautifulSoup(response.content, 'html.parser')
colonna2_td_list = soup.find_all('td', id='idx_colonna2')


for colonna2_td in colonna2_td_list:
    anchor_tags = colonna2_td.find_all('a')
    for anchor_tag in anchor_tags:
        if norm_text(disciplina) in norm_text(anchor_tag.get_text()):
            print(anchor_tag.get('href'))
 
 """
 
 