calendario.py -> codici_gare -> risultati_gara.py -> link_risultati -> scraping_risultati -> get_rankings.py -> rankings

Calendario
https://www.fidal.it/calendario.php?anno=2024&mese=1&livello=REG&new_regione=VENETO&new_tipo=3&new_categoria=PRO&submit=Invia

livello
    nessuno = 
    regionale = REG
    nazionele = COD

new_regione
    venero = VENETO
    ...

new_tipo
    nessuno = 0
    cross = 2
    indoor = 3
    outdoor = 5
    strada = 6
    ...

new_categoria
    nessuno = 
    esordienti = ESO
    ragazzi = RAG
    cadetti = CAD
    allievi = ALL
    junior = JUN
    promesse = PRO
    seniores = SEN
    master = MAS

ottenuto il codice REGXXXXX dal file HTML del calendario con calendario.py (salvato in codici_gare)
il link ai risultati della gara è uno dei seguenti

https://www.fidal.it/risultati/2024/REGXXXXX/Risultati/IndexRisultatiPerGara.html
https://www.fidal.it/risultati/2024/REGXXXXX/RESULTSBYEVENT1.htm

In base alla versione di sigma che usa la regione.

Da qui comincia il caos perché i link con i risultati della singola disciplina sono del tipo

https://www.fidal.it/risultati/2024/REG33797/Risultati/Gara722.html

solo che il numero 722 che indica in questo caso i 60HS uomini è abbastanza arbitrario e varia di gara in gara.
Quindi bisogna cercare il link dei risultati specifici in base al nome del bottone es "60Hs H106" o "60m UOMINI".
Questo rende in codice decisamente più fragile.

risultati_gara.py prende i codici gara (es. REG33797) e capisce se deve usare la versione di sigma vecchia o nuova.
Poi data una disciplina fornisce direttamente il link ai risultati di quella disciplina.
ATTENZIONE: la disciplina viene letteramente cercata con una ricerca testuale, quindi se invece che scrivere 60Hs H106
gli organizzatori hanno scritto 60HS ASSOLUTI il programma non vede la gara. Lo so, è scemo, ma per ora non ho trovato
modi più intelligenti per farlo. Per lo meno maiuscole/minuscole e spazi non contano nella ricerca (es 'salto in lungo'
viene trovato anche come 'SalToinlUNgO')

scraping_risultati.py si occupa di prendere i risultati dal link della pagina e restituire una tabella unica.
NOTA: per motivi tecnici due risultati uguali fatti nello steso giorno e caricati nel sigma nuovo vengono visti come
duplicati ed eliminati, non sapevo come altro fare.

get_ranking.py si occuperà ora di ottenere i ranking 