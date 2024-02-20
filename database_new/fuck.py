import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

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

new_url = url[:url.rfind('/')]+'/'
print(new_url)