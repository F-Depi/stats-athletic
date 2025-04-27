# Aggiornamenti live per AtleticaDB [Beta]

Questo programma permette di scaricare in live i risultati delle gare di atletica ([FIDAL](https://www.fidal.it/))
andando direttamente nella pagina sigma della gara.

## Utilizzo del Progetto

Una volta concluso, questo programma sarà in grado di fornire i dati al database utilizzato dal sito 
[AtleticaDB](https://atletica.mooo.com) per aggiornare i ranking in live, durante lo svolgimento della competizione.
Con qualche modifica, sarà anche possibile collegare i risultati presenti nel database completo, ottenuto 
[qui](https://github.com/F-Depi/database-atletica-italiana) alla gara in cui sono stati ottenuti.

## Come funziona?

Il programma funziona in più fasi:
 1. ```link_risultati.py``` scarica la lista di tutte le manifestazioni in calendario, salva il codice identificativo di
 ogni manifestazione e controlla se per quella manifestazione è già presente un pagina del sigma con i risultati.
 La lista di manifestazioni ottenute viene salvata in ```database_link/outdoor_2025/link_gare.csv```.
 Per ogni manifestazione che ha una pagina del sigma con i risultati vengono salvati tutti i link della sezione
 _risultati per gara_ e catalogati in base alla disciplina a cui corrispondono.
 Tutti questi link vengono salvati in ```database_link/outdoor_2025/link_risultati.csv```.
 Ulteriore documentazione all'interno dello script stesso.

 2. ```get_risultati.py``` si occupa quindi di scaricare tutti i risultati contenuti nei link in 
    ```database_link/outdoor_2025/link_risultati.csv``` e salvarli. Il modo in cui vengono scaricati risultati delle 
    corse e dei concorsi cambia perché cambia la struttura della pagina. Allo stesso modo la pagina del sigma vecchio è
    diversa da quella del sigma nuovo e per questo servono metodi diversi.

 3. ```???``` I risultati che ancora non sono presenti nel database generale aggiornato con
    [questo programma](https://github.com/F-Depi/database-atletica-italiana) vengono aggiunti in modo provvisorio per
    essere mostrati nel sito atletica.mooo.com in diretta (o quasi). vengono aggiunti in modo provvisorio per

## Stato attuale

 1. è quasi completato, ci sono delle difficoltà nel riconoscimento automatico della disciplina dovuto al fatto che nel
sigma vecchio non è presente da nessuna parte un nome univoco che identifichi che gara è stata corsa.

 2. Sono state costruite le funzioni per ottenere i risultati delle corse dalle pagine di sigma vecchio e nuovo,
servono ulteriori test. Devono ancora essere costruite le funzioni per ottenere i risultati dei concorsi.

 3. Facile, ma non ancora implementato. Se riesco a far funzionare il modo affidabile almeno lo scraping di risultati
dalle pagine del sigma nuovo posso già provare un'implementazione.

## TODO

 - Implementare il riconoscimento automatico della disciplina corretta per le pagine del sigma nuovo usando l'elemento
 html ```class='h7 text-danger'```

 - Implementare lo scraping dei risultati dei concorsi per il sigma nuovo. Anche in vista del fatto che prima o poi 
 tutte le regioni passeranno a quello.

 - Caricamento dei risultati del sigma nuovo nel database SQL che viene utilizzato da [AtleticaDB](atletica.mooo.com).

 - Curare la lista delle gare con i link associati in modo da poter collegare i risultati già presenti nel database SQL
 alla gara in cui sono stati conseguiti.
