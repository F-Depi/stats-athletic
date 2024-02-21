import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Generale.scrape import *


""" file1 = 'indoor_2024/link_risultati.csv'

df = pd.read_csv(file1)

for row in df.iterrows():
    
    url = row[1][5]
    
    req = requests.get(url)
    
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        if 'start' in soup.text.lower():
            print(url) """

url = 'https://www.fidal.it/risultati/2024/COD11292/Risultati/IndexRisultatiPerGara.html'

""" r = requests.get(url).text
soup = BeautifulSoup(r, 'html.parser')
elements = soup.find_all('a') # idx_link
for e in elements:
    link = e['href']
    if link[0] != '#':
        nome = e.text.strip()
        print(nome+', '+link)
 """
 
url = 'https://www.fidal.it/risultati/2024/REG33805/Index.htm'

""" new_url = url[:url.rfind('/')]+'/'
print(new_url) """

data = {
    'Codice': ['REG34144', 'REG34144', 'REG34144'],
    'Versione Sigma': ['Nuovo', 'Nuovo', 'Nuovo'],
    'Warning': ['', '', ''],
    'Disciplina': ['60m', '200m', '400m'],
    'Nome': ['60m Adulti Uomini', '200m Adulti Uomini', '400m Adulti Uomini'],
    'Link': [
        'https://www.fidal.it/risultati/2024/REG34144/Risultati/Gara001.html',
        'https://www.fidal.it/risultati/2024/REG34144/Risultati/Gara004.html',
        'https://www.fidal.it/risultati/2024/REG34144/Risultati/Gara006.html'
    ]
}

""" df = pd.DataFrame(data)

scrape_nuovo_corse(df.iloc[0,:]) """


date_str = '17 Febbraio 2024'
data_batteria = re.match(r'\b\d+ \w+ \d{4}\b', date_str)[0] # 17 gen 2024
mese_batteria = data_batteria.split()[1].lower().strip()[0:3]
print(mese_batteria)