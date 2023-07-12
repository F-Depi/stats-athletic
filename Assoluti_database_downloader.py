import time
from scarp_func import estrazione

start_time = time.time()

events = []
with open("database_events.txt", 'r') as f:
    for line in f:
        event = line.strip()[-2:]
        events.append(event)
events = events[20:37]      # selezionare l'intervallo di eventi adeguato, dal file database_events.txt

print(events)

for event in events:
    env = "I"       # I per indoor, P per outdoor
    sex = "F"       # F per donne, M per uomini
    club = ""       # codice società, lasciare vuoto per tutte le società
    mode = "1"      # 1 per le liste, 2 per le graduatorie
    folder_path = "database/database_" +sex+ "_" +env+ "_all/raw_data/Assoluti"
    estrazione(folder_path, env, sex, club, mode, event)

end_time = time.time()
execution_time = end_time - start_time

print(f"Total execution time: {execution_time} seconds")