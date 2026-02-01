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

# Check label distributions
print("\n" + "="*60)
print("LABEL DISTRIBUTION IN FULL DATASET")
print("="*60)

print("\nAttack (binary - 0/1):")
print(df['attack'].value_counts())

print("\nCategory distribution:")
print(df['category'].value_counts())

print("\nSubcategory distribution:")
print(df['subcategory'].value_counts())

# Perform stratified sampling based on 'attack' label
print("\n" + "="*60)
print("CREATING BALANCED SUBSET")
print("="*60)

# Get counts per attack label
attack_counts = df['attack'].value_counts()
print(f"\nTarget subset size: {TARGET_N:,} records")
print(f"Available records per attack label:")
print(attack_counts)

# Calculate samples per attack label (balanced)
n_labels = len(attack_counts)
samples_per_label = TARGET_N // n_labels

print(f"\nSampling ~{samples_per_label:,} records from each attack label ({n_labels} labels)")

# Perform stratified sampling using sample with stratify parameter
# Since we need balanced samples from attack labels
subsets = []
for label in df['attack'].unique():
    label_df = df[df['attack'] == label]
    sampled = label_df.sample(n=min(len(label_df), samples_per_label), random_state=RANDOM_STATE)
    subsets.append(sampled)
    print(f"  Label {label}: sampled {len(sampled):,} records")

df_subset = pd.concat(subsets, ignore_index=True)

print(f"\nSubset created:")
print(f"  Shape: {df_subset.shape}")
print(f"  Total records: {len(df_subset):,}")
print(f"\nAttack label distribution in subset:")
print(df_subset['attack'].value_counts())

print(f"\nCategory distribution in subset:")
print(df_subset['category'].value_counts())

# Save subset
print(f"\nSaving subset...")
df_subset.to_csv(OUTPUT_FILE, index=False)
print(f"✓ Saved to: {OUTPUT_FILE}")
print(f"  File size: {os.path.getsize(OUTPUT_FILE) / (1024**2):.2f} MB")
