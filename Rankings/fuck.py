from datetime import datetime

# Get today's date and format it
# today_formatted = datetime.today().date()
date = '01-02/05/2026'
date = date.replace('-','+').replace('/','-').replace('+','/')

# Output the formatted date
print(date)
