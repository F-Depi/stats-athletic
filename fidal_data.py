import requests
from bs4 import BeautifulSoup
import csv
import os

def get_data_from_url(url):
    # Make a web request to the page URL
    response = requests.get(url)

    folder_path = "database"
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
            csv_file_name = f"{folder_path}/{event_name}.csv"
            
            # Replace invalid characters with an underscore in the csv file name
            for char in r'<>:"/\|?*':
                csv_file_name = csv_file_name.replace(char, '_')
            
            # Check if the csv file already exists
            if os.path.exists(csv_file_name):
                # The csv file already exists, so open it in append mode
                csvfile = open(csv_file_name, "a", newline='', encoding='utf-8')
            else:
                # The csv file does not exist, so create it and write the header rows
                csvfile = open(csv_file_name, "w", newline='', encoding='utf-8')
                writer = csv.writer(csvfile)
                writer.writerow([event_name])
                writer.writerow(column_names)
            
            # Set start_row to 0
            start_row = 0
            
            # Create a csv writer object
            writer = csv.writer(csvfile)
            
            # Find all the table row elements
            rows = table.find_all("tr")
            
            # Loop through each table row element
            for row_index, row in enumerate(rows):
                # Skip rows before the start row
                if row_index < start_row:
                    continue
                
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
            
            # Close the csv file
            csvfile.close()
