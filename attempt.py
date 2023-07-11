from estrazione import estrazione

folder_path = "database_M_ind/raw_data"
env = "I"       # I per indoor, O per outdoor
sex = "M"       # F per donne, M per uomini
club = ""  # codice società, lasciare vuoto per tutte le società
mode = "1"      # 1 per le liste, 2 per le graduatorie
event = "01"    # empty for all (will only give first 100 results), different codes for the others. Codes are in event_code.txt

estrazione(folder_path, env, sex, club, mode, event)