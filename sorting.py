import os
import csv

def time2sec(time):
    if ':' in time:
        minutes, seconds = map(float, time.split(':'))
        return minutes * 60 + seconds
    else:
        return float(time)

folder_path = 'database_F_ind/raw_data'

for file_name in os.listdir(folder_path):
    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        sorted_rows = sorted(rows[2:], key=lambda x: time2sec(x[0]))
        output_rows = rows[:2] + sorted_rows

        output_file_name = f'sorted_{file_name}'
        output_file_path = os.path.join(folder_path.replace('raw', 'sorted'), output_file_name)

        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(output_rows)
