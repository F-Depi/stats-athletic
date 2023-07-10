from fidal_data import get_data_from_url

url = "https://www.fidal.it/graduatorie.php?anno=2022&tipo_attivita=I&sesso=M&categoria=XM&gara=0&tipologia_estrazione=1&vento=2&regione=0&nazionalita=1&limite=0&societa=bl012&submit=Invia"

get_data_from_url(url, "database_all")