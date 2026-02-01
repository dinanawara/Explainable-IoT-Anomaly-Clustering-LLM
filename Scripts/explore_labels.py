import pandas as pd
import os

# Configuration
MERGED_FILE = "/Users/nawara/Desktop/LLM-Clustering-Paper/Bot-IoT-Dataset/UNSW_2018_IoT_Botnet_Full_Merged.csv"
OUTPUT_DIR = "/Users/nawara/Desktop/LLM-Clustering-Paper/Bot-IoT-Dataset"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bot_iot_balanced_subset_300k.csv")

TARGET_N = 300000
RANDOM_STATE = 42

print("Loading merged dataset...")
df = pd.read_csv(MERGED_FILE, low_memory=False)

print(f"Full dataset shape: {df.shape}")
print(f"\nColumn names:")
print(df.columns.tolist())
print(f"\nFirst few rows:")
print(df.head())

# Check for label columns (common names: 'label', 'class', 'attack', etc.)
print(f"\nData types:")
print(df.dtypes)
