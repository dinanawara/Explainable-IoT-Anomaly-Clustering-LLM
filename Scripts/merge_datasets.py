import pandas as pd
import os

# Directory containing the CSV files
data_dir = "/Users/nawara/Desktop/LLM-Clustering-Paper/Bot-IoT-Dataset"

# List of CSV files to merge
csv_files = [
    "UNSW_2018_IoT_Botnet_Full5pc_1.csv",
    "UNSW_2018_IoT_Botnet_Full5pc_2.csv",
    "UNSW_2018_IoT_Botnet_Full5pc_3.csv",
    "UNSW_2018_IoT_Botnet_Full5pc_4.csv"
]

# Read and merge all CSV files
dfs = []
for file in csv_files:
    file_path = os.path.join(data_dir, file)
    print(f"Reading {file}...")
    df = pd.read_csv(file_path)
    print(f"  Shape: {df.shape}")
    dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save to a new CSV file
output_path = os.path.join(data_dir, "UNSW_2018_IoT_Botnet_Full_Merged.csv")
merged_df.to_csv(output_path, index=False)

print(f"\nMerging complete!")
print(f"Total rows: {len(merged_df)}")
print(f"Total columns: {len(merged_df.columns)}")
print(f"Output saved to: {output_path}")
