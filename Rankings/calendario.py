import requests
from bs4 import BeautifulSoup
import re

def extract_meet_codes_from_calendar(anno, mese, livello, regione, tipo, categoria):
    
    # Componiamo il link con i parametri del filtro
    url = 'https://www.fidal.it/calendario.php?anno='+anno+'&mese='+mese+'&livello='+livello+'&new_regione='+regione+'&new_tipo='+tipo+'&new_categoria='+categoria+'&submit=Invia'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        meet_code = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            match = re.search(fr'{livello}(\d+)', href)
            if match:
                meet_code.append(match.group(0))
        return meet_code
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return []
            
def write_to_file(codes):
    with open('codici_gare', 'w') as file:
        for code in codes:
            file.write(code + '\n')
        
url = 'https://www.fidal.it/calendario.php?anno=2024&mese=1&livello=REG&new_regione=&new_tipo=3&new_categoria=PRO&submit=Invia'  # Replace this with the URL of the webpage


"""
#Test

meet_codes = extract_meet_codes_from_calendar(url)
write_to_file(meet_codes)
print(meet_codes)
"""
