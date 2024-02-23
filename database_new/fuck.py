import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from Generale.scrape import *

""" data = {
    'Codice': ['REG34127', 'REG34144', 'REG34144'],
    'Versione Sigma': ['Vecchio', 'Nuovo', 'Nuovo'],
    'Warning': ['', '', ''],
    'Disciplina': ['1000m', '200m', '400m'],
    'Nome': ['1000 metri Master Uomini', '200m Adulti Uomini', '400m Adulti Uomini'],
    'Link': [
        'https://www.fidal.it/risultati/2024/REG34127/Gara009.htm',
        'https://www.fidal.it/risultati/2024/REG34144/Risultati/Gara004.html',
        'https://www.fidal.it/risultati/2024/REG34144/Risultati/Gara006.html'
    ]
}

df = pd.DataFrame(data)
df = scrape_vecchio_corse(df.iloc[0,:]) """

df1 = pd.read_csv('TEST_vecchio.csv')
df2 = pd.read_csv('TEST_vecchio2.csv')
for (ii,a), (ii,b) in zip(df1.iterrows(), df2.iterrows()):
    #if ii>1356:
        if df1.iloc[ii,2] != df2.iloc[ii,2]:
            print(ii+2)
            break
    
