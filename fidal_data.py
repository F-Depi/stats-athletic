import csv
import os
import requests
from bs4 import BeautifulSoup

def get_data_from_url(url, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    header_row = None
    year = None
    column_names = ["Tempo", "Vento", "Atleta", "Età", "Società", "Posizione", "Luogo", "Data"]
    
    for table_index, table in enumerate(soup.find_all("table")):
        if table_index % 2 == 0:
            header_cells = [cell.text.strip() for cell in table.find_all(["td", "th"])]
            header_row = [header_cells[0]]
            year = header_cells[1].split(":")[-1]
        else:
            event_name = header_row[0]
            csv_file_name = f"{event_name}.csv"
            for char in r'<>:"/\|?*':
                csv_file_name = csv_file_name.replace(char, '_')
                
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
                    writer.writerow(row_data)

