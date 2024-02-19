import pandas as pd
import requests
from bs4 import BeautifulSoup

file1 = 'indoor_2024/link_risultati.csv'

df = pd.read_csv(file1)

for row in df.iterrows():
    
    url = row[1][5]
    
    req = requests.get(url)
    
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        if 'start' in soup.text.lower():
            print(url)