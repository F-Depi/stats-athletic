import pandas as pd
import csv
import json
import os

## File utilizzato per creare la prima versione del dizionario. Ora serve solo ad aggiornare con le cose nuove che escono da run_me.py

file_dizionario = 'Generale/event_dict.json'
file_dizionario_new = 'Generale/event_dict_new.json'

def merge_dict(file1, file2):
    
    ## funzione per unire 2 file .json
    ## gli elementi in file2 vengono copiari in file1 e file2 viene eliminato
    
    with open(file1, 'r') as f1:
        dict1 = json.load(f1)

    with open(file2, 'r') as f2:
        dict2 = json.load(f2)

    # Merge the dictionaries
    dict1.update(dict2)
    
    with open(file1, 'w') as f3:
        json.dump(dict1, f3, sort_keys=True, indent=4)
    
    os.remove(file2)
    
    return

merge_dict(file_dizionario, file_dizionario_new)

""" ## Dizionario per tradurre i nomi vari che vengono dati agli eventi (es '60Hs Donne', '60 Hs H84 J/P/S Donne', '60Hs H84-8.50 JUNIORES-PROMESSE-SENIORES FEMMINILI')
## in un nome standard che indetifichi univocamente la disciplina (es '60 Hs h84-8.50')
## Sono sostanzialmente fatti a mano guardando tutti quelli che get_results_links ha trovato nelle gare.

file_dizionario = 'Generale/event_dict.json'
file_20XX = 'indoor_2019/link_risultati_key.csv'
discipline = []
nomi = []
for X in range(19, 25):
    file_20XX = 'indoor_20'+str(X)+'/link_risultati_key.csv'
    with open(file_20XX, 'r', newline='') as f1: #apro il dizionario
        reader = csv.reader(f1)
        for row in reader:
            disciplina = row[2]
            nome = row[3]
            discipline.append(disciplina)
            nomi.append(nome)
            
print(str(len(nomi)) + '\teventi totali dal 2019 al 2024')

dumb_dict = {}
for disciplina, nome in zip(discipline, nomi):
    if nome not in dumb_dict:
        dumb_dict[nome] = [disciplina]

print(str(len(dumb_dict)) + '\teventi con nome unico dal 2019 al 2024')

## Now let's try to work smarter

def hard_strip(nome_str):
    # takes a str as input with the name given to a discipline in a meet
    # does its best to remove unecessary words and character
    # output is the same str, hopefully a shorter and more standard version
    # without loosing any useful informations
    
    nome_str = nome_str.strip().lower()
    if nome_str.startswith('modello 1'): return 'altro'
    if nome_str.startswith('1/sta'): return 'altro'
    nome_str = nome_str.replace('(', ' ').replace(')', ' ')
    
    first_trash = ['finale','extra','ad invito','invito','piani','staffetta','staff.',' u14 ',' u15 ',' u16 ',' u17 ',' u18 ',' u19 ',' u19 ',' u20 ',' u23 ']
    for word in first_trash:
        nome_str = nome_str.replace(word, '')
    
    nome_str = nome_str.replace('metri','m').replace('ostacoli','hs')
    
    second_trash = ['salto con l\'','salto in','salto']
    for word in second_trash:
        if nome_str.startswith(word):
            nome_str = nome_str.replace(word, '')
    
    third_trash = [' ','/','bancari','indoor']
    for word in third_trash:
        nome_str = nome_str.replace(word, '')
        
    fourth_trash = ['asta','lungodafermo','lungo','alto','triplo','quadruplo']
    for word in fourth_trash:
        if nome_str.startswith(word):
            nome_str = word
    
    fifth_trash = ['pesokg1','pesokg2','pesokg3','pesokg4','pesokg5','pesokg6','pesokg7.260','pesospkg1','pesospkg2','pesospkg3','pesospkg4','pesospkg5','pesospkg6','pesospkg7.260']
    for word in fifth_trash:
        if nome_str.startswith(word):
            nome_str = word
            
    return nome_str


smart_dict = {}
for disciplina, nome in zip(discipline, nomi):
    nome = hard_strip(nome)
    if nome not in smart_dict:
        smart_dict[nome] = disciplina

print(str(len(smart_dict)) + '\teventi filtrati con hard_strip() dal 2019 al 2024')


#for nome, disciplina in smart_dict.items():
#    print(f"{nome}: {disciplina}") 


with open(file_dizionario, 'w') as f1:
    json.dump(smart_dict, f1, sort_keys=True, indent=4)
 """
