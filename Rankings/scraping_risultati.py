from bs4 import BeautifulSoup
import requests
import csv
import re

def extract_results_from_html(url, output_file):
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    """     # Trova l'indice della parola "Riepilogo"
    index_riepilogo = html_content.find('RIEPILOGO')
    print(index_riepilogo)

    # Se trova la parola "Riepilogo", rimuove tutto ciò che precede
    if index_riepilogo != -1:
        html_content = html_content[index_riepilogo:]
    print(html_content) """
        
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with class 'tab_turno'
    tables = soup.find_all('table', class_='tab_turno')

    # Open a CSV file in write mode
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        
        # Write the header row
        writer.writerow(['Athlete', 'Year', 'Category', 'Club', 'Performance', 'Points'])

        # Iterate over each table (each representing a round)
        for table in tables:
            # Find all rows in the table
            rows = table.find_all('tr')

            # Iterate over each row in the table, skipping the header row
            for row in rows[1:]:
                # Extract text from each cell in the row
                cells = row.find_all('td')
                
                # Check if the cells list has enough elements
                if len(cells) >= 9:
                    # Extract only the required fields
                    athlete = cells[3].text.strip()
                    year = cells[4].text.strip()
                    category = cells[5].text.strip()
                    club = cells[6].text.strip()
                    performance_text = cells[7].text.strip()
                    performance = ''.join(char for char in performance_text if char.isdigit() or char in ['.', ','])
                    performance = performance.replace(',', '.')  # Replace comma with dot for decimal point
                    performance = float(performance) if performance else None
                    points = cells[8].text.strip()

                    # Write the data to the CSV file
                    writer.writerow([athlete, year, category, club, performance, points])

            

# URL of the page containing the results
url = 'https://www.fidal.it/risultati/2024/REG33677/Gara120.htm'

# Output file path
output_file = 'results.csv'

# Call the function to extract and write results to CSV
extract_results_from_html(url, output_file)

