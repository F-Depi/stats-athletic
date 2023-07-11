from fidal_data import get_data_from_url
from sorting import raw_sorting

# This scrpts, if in the same folder of the function it calls (fidal_data and sorting), gets all the data you need from fidal.it. You can select the parameters
# to choose wich data you want to download and where in your PC.

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
    years = [str(year) for year in range(2005, 2024)]
    for year in years:
        url_year = url.replace("year", year)
        get_data_from_url(url_year, folder_path)


    # Sorting the data
    raw_sorting(folder_path)