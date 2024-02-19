import csv
import os
import re
import requests
from bs4 import BeautifulSoup

# this is the function that gets the data from the web, given a link
def get_data_from_url(url, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    for table_index, table in enumerate(soup.find_all("table")):
        
        #first we take event name, year and enviroment from the even tables
        if table_index % 2 == 0:
            header_cells = [cell.text.strip() for cell in table.find_all(["td", "th"])]
            event_name = header_cells[0]
            year = header_cells[1].split(":")[-1]
            env = header_cells[3].split(":")[-1]
            csv_file_name = f"{event_name}.csv"
            for char in r'<>:"/\|?*':
                csv_file_name = csv_file_name.replace(char, '_')
        
        # now the actual data from the odd tables
        else:

            # takes out the wind from events where it isn't measured
            if env == "Outdoor" and any(event in event_name for event in ["60", "80", "100", "110", "150", "200", "lungo", "triplo"]) and not any(event in event_name for event in ["800", "1000", "1500", "10000", "2000","+"]):
                column_names = ["Prest.", "Vento", "Atleta", "Anno", "Società", "Città", "Data"]
                wind = True
            else:
                column_names = ["Prest.", "Atleta", "Anno", "Società", "Città", "Data"]
                wind = False
            
            file_exists = os.path.exists(f"{folder_path}/{csv_file_name}")
            with open(f"{folder_path}/{csv_file_name}", "a" if file_exists else "w", newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(column_names)
                
                for row in table.find_all("tr"):
                    cells = row.find_all(["td", "th"])
                    
                    # Check if the row has only one cell and if that cell is a th element
                    if len(cells) == 2:
                        # Skip this row and continue with the next one
                        continue
                    
                    row_data = [cell.text.strip() if cell_index != len(cells) - 1 else f"{cell.text.strip()}/{year}" for cell_index, cell in enumerate(cells)]
                    del row_data[5]
                    if wind == False:
                        del row_data[1]
                    writer.writerow(row_data)


# These 2 are used to order the data downloaded
def min2sec(time):
    try:
        if time == "5:50:01":                 # database typo in ZAMBELLI Beatrice...
            total_seconds = 350
        elif time == "1.08.66":
            total_seconds = 0
        elif time == "8.13.9":
            total_seconds = 0
        elif any(typo in time for typo in ["-", "X", "R", "P"]):                     # database typo or something weird in jumps
            total_seconds = 0
        elif "h" in time:
            hours, minutes, seconds = re.findall(r"(\d+)h(\d+):(\d+)", time)[0]
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        elif ":" in time:
            time_parts = list(map(float, time.split(":")))
            if len(time_parts) == 3:
                hours, minutes, seconds = time_parts
                total_seconds = hours * 3600 + minutes * 60 + seconds
            elif len(time_parts) == 2:
                minutes, seconds = time_parts
                total_seconds = minutes * 60 + seconds
        else:
            total_seconds = float(time)
        if len(time.split(".")[-1]) == 1:       # manual to electrical time conversion, +0.24s
            total_seconds += 0.24
        return total_seconds
    except Exception as e:                      # I have no idea
        print(f"Error in converting time: {time}\n{str(e)}")
        return 0
    
def raw_sorting(in_folder):

    out_folder = in_folder.replace('raw_data', 'lists')
    os.makedirs(out_folder, exist_ok=True)

    for file_name in os.listdir(in_folder):
        with open(f'{in_folder}/{file_name}','r') as in_f:
            data = list(csv.reader(in_f))
        rev_order = False
        concorsi = ["Salto", "Peso", "Disco", "Giavellotto", "Martello", "\'", "PENTATHLON", "EPTATHLON", "OCTATHLON", "DECATHLON"]
        if any(concorso in file_name for concorso in concorsi):
            rev_order = True
        sorted_data = sorted(data[1:], key=lambda row: min2sec(row[0]), reverse=rev_order)
        sorted_data = [data[0]] + sorted_data
        
        with open(f'{out_folder}/list_{file_name}', 'w', newline='') as out_f:
            writer = csv.writer(out_f)
            writer.writerows(sorted_data)

# This one uses the funtions above to get all the data you need from fidal.it.
# You can select the parameters to choose wich data you want to download and where in your PC.
def estrazione(folder_path, env, sex, club, mode, event):
    # Initial parameters
    '''
    folder_path = "database_M_ind/raw_data"
    env = "I"       # I per indoor, O per outdoor
    sex = "M"       # F per donne, M per uomini
    club = ""  # codice società, lasciare vuoto per tutte le società
    mode = "1"      # 1 per le liste, 2 per le graduatorie
    event = ""    # empty for all (will only give first 100 results), different codes for the others. Codes are in event_code.txt
    '''
    # Preparing the general link to scrape from
    url = "https://www.fidal.it/graduatorie.php?anno=year&tipo_attivita=env&sesso=sex&categoria=Xsex&gara=event&tipologia_estrazione=mode&vento=2&regione=0&nazionalita=1&limite=&societa=club&submit=Invia"
    url = url.replace('env', env)
    url = url.replace('sex', sex)
    url = url.replace('club', club)
    url = url.replace('mode', mode)
    url = url.replace('event', event)

    # Extracting the data from fidal.it
    years = [str(year) for year in range(2005, 2025)]
    for year in years:
        url_year = url.replace("year", year)
        get_data_from_url(url_year, folder_path)


    # Sorting the data
    raw_sorting(folder_path)
