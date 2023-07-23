from scarp_func import estrazione

envs = ["I", "P"]       # I per indoor, P per outdoor
sexs = ["F","M"]       # F per donne, M per uomini

for env in envs:
    for sex in sexs:
        club = "bl012"  # codice società, lasciare vuoto per tutte le società
        mode = "1"      # 1 per le liste, 2 per le graduatorie
        event = ""    # empty for all (will only give first 100 results), different codes for the others. Codes are in event_code.txt
        folder_path = "database_ANA/assoluti/database_" +sex+ "_" +env+ "_" +club+ "/raw_data"

        estrazione(folder_path, env, sex, club, mode, event)