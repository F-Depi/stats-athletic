from fidal_data import get_data_from_url
from sorting import raw_sorting

# This scrpts, if in the same folder of the function it calls (fidal_data and sorting), gets all the data you need from fidal.it. You can select the parameters
# to choose wich data you want to download and where in your PC.

# Initial parameters
years = [str(year) for year in range(2005, 2024)]
folder_path = "database_F_ind/raw_data"
env = "I"       # I per indoor, O per outdoor
sex = "F"       # F per donne, M per uomini
club = ""  # codice società, lasciare vuoto per tutte le società
mode = "1"      # 1 per le liste, 2 per le graduatorie

# Preparing the general link to scrape from
url = "https://www.fidal.it/graduatorie.php?anno=year&tipo_attivita=env&sesso=sex&categoria=Xsex&gara=&tipologia_estrazione=mode&vento=2&regione=0&nazionalita=1&limite=0&societa=club&submit=Invia"
url = url.replace('env', env)
url = url.replace('sex', sex)
url = url.replace('club', club)
url = url.replace('mode', mode)

# Extracting the data from fidal.it
for year in years:
    url_year = url.replace("year", year)
    get_data_from_url(url_year, folder_path)


# Sorting the data
raw_sorting(folder_path)