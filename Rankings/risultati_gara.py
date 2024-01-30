import requests
from bs4 import BeautifulSoup
import re

def extract_link_of_discipline_results(meet_code, disciplina):
    url = 'https://www.fidal.it/risultati/2024/' + meet_code + '/'
    url1 = url + 'Risultati/IndexRisultatiPerGara.html'
    url2 = url + 'RESULTSBYEVENT1.htm'
    url3 = url + 'Index.htm'

    if (requests.get(url1).status_code == 200) or (requests.get(url2).status_code == 200) or (requests.get(url3).status_code == 200):                       # Controllo che la richiesta abbia successo
        
        html_content1 = requests.get(url1).text
        html_content2 = requests.get(url2).text
        html_content3 = requests.get(url3).text
        
        norm_disciplina = disciplina.lower().replace(' ', '')  # Normalize discipline text
        
        if not("Errore 404" in html_content1):                      # controllo se è il sigma nuovo ed estraggo
            soup = BeautifulSoup(html_content1, 'html.parser')
            links = soup.find_all('a', href=True)
            href_list = []
            for link in links:
                link_text = link.get_text().strip().lower().replace(' ', '')  # Normalize link text
                if link_text.startswith(norm_disciplina):  # Check if link text starts with normalized discipline text
                    href = link['href'] # Gara220.html
                    href_list.append(url + 'Risultati/' + href)
            
            print(meet_code + ' Sigma Nuovo')
            return href_list
        
        elif not("Errore 404" in html_content2):                    # controllo se è il sigma vecchio ed estraggo
            soup = BeautifulSoup(html_content2, 'html.parser')
            links = soup.find_all('a', href=True)
            href_list = []
            for link in links:
                link_text = link.get_text().strip().lower().replace(' ', '')  # Normalize link text
                if link_text.startswith(norm_disciplina):  # Check if link text starts with normalized discipline text
                    href = link['href']
                    href_list.append(url + href)
            
            print(meet_code + ' Sigma Vecchio')
            return href_list
        
        elif not("Errore 404" in html_content3):                    # controllo se è il sigma vecchissimo ed estraggo
            soup = BeautifulSoup(html_content3, 'html.parser')
            td_elements = soup.find_all('td', {'id': 'idx_colonna2'}, string=lambda text: disciplina.replace(" ", "").lower() in text.replace(" ", "").lower())
            links = [td.find('a')['href'] for td in td_elements] # Extract the link attribute from each <a> element
            href_list = []
            for href in links:
                href_list.append(url + href)
            
            print(meet_code + ' Sigma Vecchissimo')
            return href_list
        
        else:                                                       # se la gara non esiste dovrei arrivare qui
            print(meet_code + ' C\'è qualcosa che non va')
            return[]
    else:
        print(meet_code + f" Errore {requests.get(url1).status_code}: Gara annullata, da svolgersi o pagina non raggiungibile")   # se il server non risponde
        return []



def norm_text(text):                                         # questa serve perché ognuno scrive le cose un po'
    # Rimuove gli spazi extra e converte in minuscolo                 come cazzo gli pare
    return re.sub(r'\s+', '', text.strip().lower())


"""
# Test
disciplina = '60hs H106'
links = []
with open('codici_gare', 'r') as file1:
    for code in file1:
        code = code.strip()
        link = extract_link_of_discipline_results(code,disciplina)
        print(link)
        if link:
            links.extend(link)

with open('link_risultati', 'w') as file2:
    for link in links:
        file2.write(link + '\n')
"""

