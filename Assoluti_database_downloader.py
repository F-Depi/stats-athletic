import time
from scarp_func import estrazione

start_time = time.time()

events = []
with open("event_code.txt", 'r') as f:
    for line in f:
        event = line.strip()[-2:]
        events.append(event)
events = events[0:12]

for event in events:
    env = "I"       # I per indoor, P per outdoor
    sex = "M"       # F per donne, M per uomini
    club = ""       # codice società, lasciare vuoto per tutte le società
    mode = "1"      # 1 per le liste, 2 per le graduatorie
    event = "28"    # empty for all (will only give first 100 results), different codes for the others. Codes are in event_code.txt
    folder_path = "database/database_" +sex+ "_" +env+ "_all/raw_data"

estrazione(folder_path, env, sex, club, mode, event)

end_time = time.time()
execution_time = end_time - start_time

print(f"Total execution time: {execution_time} seconds")