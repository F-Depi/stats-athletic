import pandas as pd

url = 'https://www.fidal.it/risultati/2024/REG33797/Risultati/Gara722.html'
dfs = pd.read_html(url)
for df in dfs:
    societa_column = 'Società' if 'Società' in df.columns else 'CLUB'
    print(societa_column)