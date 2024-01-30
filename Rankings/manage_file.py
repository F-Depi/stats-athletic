import os

def write_file(output_file, data):
    directory = os.path.dirname(output_file)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(output_file, 'w') as file:
        for line in data:
            file.write(line + '\n')
    return[]
            

def read_file(input_file):
    data=[]
    with open(input_file, 'r') as file:
        for line in file:
            data.append(line.strip())
    return(data)
