import pandas as pd
import os
from func_general import extract_meet_codes_from_calendar, get_meet_info, get_events_link
from func_assegnazione_evento import assegna_evento_generale, assegna_evento_specifico
import time
start_time = time.time()


anno = '2024';      regione = '';       categoria = ''      
mese = '';          tipo = '3'

#for anno in range(2011, 2025):
#    anno = str(anno)
#folder_link = 'database_link/indoor_'+anno+'/'
folder_link = 'test/'
file_gare = folder_link + 'link_gare.csv'
file_risultati = folder_link + 'link_risultati.csv'
file_dizionario = 'Generale/event_dict.json'
file_dizionario_new = 'Generale/event_dict_new.csv'


################# Codici gare (anno, mese, livello, regione, tipo, categoria) ###################
## Se file_gare è già presente viene solo aggiornato con i nuovi codici gara
## la funzione usata restituisce un DataFrame columns=['Data', 'Codice', 'Ultimo Aggiornamento', 'Nome', 'Home Gara']
print('---------------------------------------------')

df_REG_gare = extract_meet_codes_from_calendar(anno,mese,'REG',regione,tipo,categoria)
df_COD_gare = extract_meet_codes_from_calendar(anno,mese,'COD',regione,tipo,categoria)
df_gare = pd.concat([df_REG_gare, df_COD_gare], ignore_index=True)
df_gare[['Home','Risultati','Versione Sigma','Status']] = ''
df_gare = df_gare[['Data','Codice','Nome','Home Gara','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']]

# Aggiornamento file
if not os.path.exists(folder_link): os.makedirs(folder_link)

if os.path.exists(file_gare):

    print('E\' stato trovato il file ' + file_gare)

    df_gare_old = pd.read_csv(file_gare, sep='\t')
    df_gare_old['Data'] = pd.to_datetime(df_gare_old['Data']).dt.date
    df_gare_old['Ultimo Aggiornamento'] = pd.to_datetime(df_gare_old['Ultimo Aggiornamento']).dt.date

    df_gare_new = df_gare[~df_gare['Codice'].isin(df_gare_old['Codice'])]
    df_gare = pd.concat([df_gare_old, df_gare_new], ignore_index=True)

    if len(df_gare_new) > 0:
        print('Sono stati aggiunti i codici gare:\n')
        for cod in df_gare_new['Codice']: print(cod + '\n')

    else: print('Non sono stati aggiunti codici gare\n')

else: print('Non ho trovato il file ' + file_gare + ', lo creo con i '+str(len(df_gare))+' codici gare trovati.')

## Mettiamo le gare in ordine cronologico
df_gare = df_gare.sort_values(by='Data')
df_gare = df_gare.reset_index(drop=True)

#################################################################################################



################# Link ai risultati (Codici delle gare, Disciplina scelta)   ####################
## In modalità 'date' aggiorna il DataFrame delle gare controllando se sono disponibili nuovi link nelle gare
## che hanno |data_gara - data_oggi| < 7 giorni oppure delle gare passate che hanno
## (data_ultimo_aggiornamento - data_gara) < 7 giorni
## Il DataFrame deve essere già del tipo:
## ['Data','Codice','Home','Risultati','Versione Sigma','Status','Ultimo Aggiornamento']
print('---------------------------------------------')
update_condition = 'date_5'

df_gare = get_meet_info(df_gare, update_condition)
df_gare.to_csv(file_gare, sep='\t', index=False)

##################################################################################################


exit()
################# Otteniamo i link a ogni risultato di ogni disciplina per ogni gara #############
## usiamo come DataFrame ['Codice', 'Versione Sigma', 'Disciplina', 'Nome', 'Link']
## per ora ci occupiamo solo di trovare 'Nome' e 'Link'
## get_events_link() prende i link trovati prima e tira fuori i link alle pagine di risultati delle
## singole discipline. Aggiorna il file se lo trova.
## NOTA: il criterio di aggiornamento è solo quello di aggiornare gare finite da meno di N giorni.
## Quindi gare più vecchie non vengono aggiornate, nel bene o nel male. Dovrei aggiungere un'altra
## colonna con 'Ultimo Aggiornamento', ma non oggi.
print('\n---------------------------------------------')
print('Ora cerco i link agli eventi di ogni gara')

update_condition = 'date_5'

if os.path.exists(file_risultati):

    print('Ho trovato il file di risultati '+file_risultati+', aggiorno questo.')
    df_risultati_old = pd.read_csv(file_risultati)

    df_risultati = get_events_link(df_gare, update_condition, df_risultati_old)

else:
    print('Non ho trovato il file ' + file_risultati + ', lo creo.')
    df_risultati = get_events_link(df_gare,'ok')

df_risultati = df_risultati.drop_duplicates(subset=['Link'])
df_risultati.to_csv(file_risultati, index=False)



################# Identifichiamo la disciplina corretta con il dizionari dei nomi #################
## molto del lavoro sul dizionario è stato inizialmente fatto a mano, poi gestito in dizionario.py
## I nomi dati alle discipline, che variano in base a quello che sceglie l'organizzatore della gara,
## vengono "puliti" dalla funzione hard_strip() per ridurre le dimensioni del dizionario.
## Il rischio di errore in questa parte è alto a causa di typo miei, nomi molto ambigui, hard_strip()
## che incontra un nome così strano che tolta qualche lettera diventa una disciplina diversa (ho fatto
## in modo che questa cosa sia improbabile)
""" print('---------------------------------------------')
print('Applico il dizionario per dare il nome corretto agli eventi')

with open(file_dizionario, 'r') as f1:
    event_dict = json.load(f1)

eventi_ignoti = []
for ii, row in df_risultati.iterrows():

    nome = row['Nome']
    nome = hard_strip(nome)

    if nome in event_dict:
        df_risultati.loc[ii, 'Disciplina'] = event_dict[nome]
    else:
        print('\nNon conosco ' + nome)
        eventi_ignoti.append([nome, 'boh'])

df_risultati.to_csv(file_risultati_key, index=False)

if eventi_ignoti:
    with open(file_dizionario_new, 'w') as f2:
        f2.write('Nome,Disciplina\n')
        for a, b in eventi_ignoti:
            f2.write(a+','+b+'\n') """


for ii, row  in df_risultati.iterrows():

    nome = df_risultati.loc[ii,'Nome']
    disciplina = df_risultati.loc[ii,'Disciplina']
    link = df_risultati.loc[ii, 'Link']
    nome = str(nome)
    disciplina = str(disciplina).strip()
    link = str(link)

    #if disciplina == 'boh':

    eve_gen = ''
    warn_gen = ''
    eve_spec = ''
    eve_gen = ''

    (eve_gen, warn_gen) = assegna_evento_generale(nome, link)
    (eve_spec, warn_spec) = assegna_evento_specifico(nome, eve_gen)

    df_risultati.loc[ii,'Disciplina'] = eve_spec
    df_risultati.loc[ii,'Warning'] = (warn_gen+' '+warn_spec).strip()


print("--- %s secondi ---" % round(time.time() - start_time, 2))
df_risultati.to_csv(file_risultati, index=False)
