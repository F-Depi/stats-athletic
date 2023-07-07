import requests
from bs4 import BeautifulSoup
import csv

# Make a web request to the page URL
url = "https://www.fidal.it/graduatorie.php?anno=2022&tipo_attivita=I&sesso=M&categoria=XM&gara=&tipologia_estrazione=1&vento=2&regione=0&nazionalita=1&limite=0&societa=bl012&submit=Invia"
response = requests.get(url)

# Create a soup object from the response content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the table elements in the HTML content
tables = soup.find_all("table")

# Initialize variables to store the header row and year
header_row = None
year = None

# Specify the column names for each csv file
column_names = ["Tempo", "Vento", "Atleta", "Età", "Società", "Posizione", "Luogo", "Data"]

# Loop through each table element
for table_index, table in enumerate(tables):
    # Check if this is an even-indexed table (0, 2, 4, ...)
    if table_index % 2 == 0:
        # This is a header table, so extract the header row and year
        header_cells = [cell.text.strip() for cell in table.find_all(["td", "th"])]
        header_row = [header_cells[0]]
        year = header_cells[1].split(":")[-1]
    else:
        # This is a data table, so create a csv file for this event
        event_name = header_row[0]
        csv_file_name = f"{event_name}.csv"
        
        # Replace invalid characters with an underscore in the csv file name
        for char in r'<>:"/\|?*':
            csv_file_name = csv_file_name.replace(char, '_')
        
        # Open the csv file in write mode
        with open(csv_file_name, "w", newline='', encoding='utf-8') as csvfile:
            # Create a csv writer object
            writer = csv.writer(csvfile)
            
            # Write the event name to the first line of the csv file
            writer.writerow([event_name])
            
            # Write the column names to the second line of the csv file
            writer.writerow(column_names)
            
            # Find all the table row elements
            rows = table.find_all("tr")
            
            # Loop through each table row element
            for row in rows:
                # Find all the table cell elements
                cells = row.find_all(["td", "th"])
                
                # Create an empty list to store the row data
                row_data = []
                
                # Loop through each table cell element
                for cell_index, cell in enumerate(cells):
                    # Get the text content of the cell
                    cell_text = cell.text.strip()
                    
                    # Check if this is the last cell (date column)
                    if cell_index == len(cells) - 1:
                        # Append the year to the date and add it to the row data list
                        cell_text = f"{cell_text}/{year}"
                    
                    # Append the cell text to the row data list
                    row_data.append(cell_text)
                
                # Write the row data to the csv file
                writer.writerow(row_data)
