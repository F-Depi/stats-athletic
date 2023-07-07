from fidal_data2 import get_data_from_url

year = ["2019", "2020", "2021", "2022", "2023"]
url = "https://www.fidal.it/graduatorie.php?anno=2023&tipo_attivita=P&sesso=M&categoria=XM&gara=&tipologia_estrazione=1&vento=2&regione=0&nazionalita=1&limite=0&societa=&submit=Invia"

for a in year:
    url_a = url.replace("2023", a)
    folder_path = "database_all"
    #print(url)
    get_data_from_url(url, folder_path)

