import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

""" ef norm_text(text):                                         # questa serve perché ognuno scrive le cose un po'
    # Rimuove gli spazi extra e converte in minuscolo                 come cazzo gli pare
    return re.sub(r's+', '', text.strip().lower())


meet_code = 'REG33752'
url = 'https://www.fidal.it/risultati/2024/' + meet_code + '/'
url3 = url + 'Index.htm'
disciplina = '60hsh106'

html_content3 = requests.get(url3).text

# Parse the HTML content
soup = BeautifulSoup(html_content3, 'html.parser')

# Find all <td> elements with id='idx_colonna2' containing the specified text
td_elements = soup.find_all('td', {'id': 'idx_colonna2'}, string=lambda text: disciplina.replace(" ", "").lower() in text.replace(" ", "").lower())

# Extract the href attribute from each <a> element
links = [td.find('a')['href'] for td in td_elements]

# Print the links
print(links) """





temp_df = pd.DataFrame(columns=['Codice', 'Home', 'Risultati', 'Versione Sigma', 'Status'])
temp_df.loc[0] = ['', '', '', '', '']








































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
 
 