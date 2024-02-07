import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def extract_meet_codes_from_calendar(anno, mese, livello, regione, tipo, categoria):
    
    # Componiamo il link con i parametri del filtro
    url = 'https://www.fidal.it/calendario.php?anno='+anno+'&mese='+mese+'&livello='+livello+'&new_regione='+regione+'&new_tipo='+tipo+'&new_categoria='+categoria+'&submit=Invia'
    response = requests.get(url)
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='table_btm')
        
        dates = []
        meet_code = []
        
        # These have text with the date of the meet
        b_elements = div.find_all('b')
        for b in b_elements:
            if 'title' in b.attrs:
                date = b.get_text(strip=True)
                date = date + '/' + anno
                dates.append(date)
        
        # These have the link with the meet code
        a_elements = div.find_all('a', href=True)
        for a in a_elements:
            href = a['href']
            match = re.search(fr'{livello}(\d+)', href)
            if match:
                meet_code.append(match.group(0))
            
        df = pd.DataFrame({'Data': dates, 'Codice': meet_code})
        
        return df
    
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return []
            
def write_to_file(codes):
    with open('codici_gare', 'w') as file:
        for code in codes:
            file.write(code + '\n')
        



#Test

meet_codes = extract_meet_codes_from_calendar('2024','1','REG','','3','')
print(meet_codes)

