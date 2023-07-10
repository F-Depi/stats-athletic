from fidal_data import get_data_from_url

years = [str(year) for year in range(2005, 2024)]

url = "https://www.fidal.it/graduatorie.php?anno=2023&tipo_attivita=I&sesso=F&categoria=XF&gara=&tipologia_estrazione=1&vento=2&regione=0&nazionalita=1&limite=0&societa=bl012&submit=Invia"

for year in years:
    url_year = url.replace("2023", year)
    folder_path = "database_F_ind/raw_data"
    #print(url)
    get_data_from_url(url_year, folder_path)

