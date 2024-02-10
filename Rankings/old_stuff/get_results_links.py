import pandas as pd
import requests
from bs4 import BeautifulSoup


file_links = 'Generale/link_gare.csv'
file_links_results = 'Generale/link_risultati_gare.csv'
df_links = pd.read_csv(file_links, sep='\t')

df_links_results = pd.DataFrame(columns=['Versione Sigma', 'Disciplina', 'Link'])


# Link al sigma NUOVO
df_links_nuovi = df_links[(df_links['Versione Sigma'] == 'Nuovo') & (df_links['Status'] == 'ok')]
for url in df_links_nuovi['Risultati']:
    
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    elements = soup.find_all('div', class_='col-md-6')  # classe della div dove ci sono i link ai risultati
    
    for element in elements:
        anchor = element.find('a')
        
        if anchor:  # non ho idea di cosa sia anchor, ma a quanto pare ogni tanto è vuoto
            link = anchor['href']
            link = url[:-26] + link
            text = anchor.text.strip()
            data = pd.DataFrame([{'Versione Sigma':'Nuovo', 'Disciplina':text, 'Link':link}])
            df_links_results = pd.concat([df_links_results, data])
            #df_links_results = df_links_results.append(, ignore_index=True)


# Link al sigma VECCHIO
df_links_vecchi = df_links[(df_links['Versione Sigma'] == 'Vecchio') & (df_links['Status'] == 'ok')]
for url in df_links_vecchi['Risultati']:
    
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    elements = soup.find_all('td', id='idx_colonna1')

    for element in elements:
        a_tag = element.find('a')
        if a_tag:
            link = a_tag['href']
            link = url[:-19] + link
            text = a_tag.get_text(strip=True)
            data = pd.DataFrame([{'Versione Sigma':'Vecchio', 'Disciplina':text, 'Link':link}])
            df_links_results = pd.concat([df_links_results, data])


# Link al sigma VECCHISSIMO
df_links_vecchissimi = df_links[(df_links['Versione Sigma'] == 'Vecchissimo') & (df_links['Status'] == 'ok')]
for url in df_links_vecchissimi['Risultati']:
    
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    elements = soup.find_all('td', id='idx_colonna2')
    
    for element in elements:
        a_tag = element.find('a')
        if a_tag:
            link = a_tag['href']
            link = url[:-9] + link
            text = a_tag.get_text(strip=True)
            data = pd.DataFrame([{'Versione Sigma':'Vecchissimo', 'Disciplina':text, 'Link':link}])
            df_links_results = pd.concat([df_links_results, data])
    

# Salviamo tutto
df_links_results.to_csv(file_links_results, index=False)