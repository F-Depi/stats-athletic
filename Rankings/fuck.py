import pandas as pd
import os

def merge_csv_files(output_file, N1, N2):
    # List all files starting with the given prefix
    files = [f"indoor_{num}/link_risultati.csv" for num in range(N1, N2+1)]
    
    # Read the first file to initialize the DataFrame
    df = pd.read_csv(files[0])
    
    # Iterate over remaining files and append them to the DataFrame
    for file in files[1:]:
        df = df.append(pd.read_csv(file), ignore_index=True) # I know
    
    # Write the merged DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# Define the number of files (N)
N1 = 2018  # Change this number to the actual number of files
N2 = 2024

# Call the function to merge CSV files
merge_csv_files("merged_links.csv", N1, N2)
