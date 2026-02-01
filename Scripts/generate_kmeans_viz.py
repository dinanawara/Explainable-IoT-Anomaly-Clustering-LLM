#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("K-MEANS 3D VISUALIZATION GENERATOR")
print("=" * 80)

print("\n1. Loading data...")
data_path = "/Users/nawara/Desktop/LLM-Clustering-Paper/Data/Bot-IoT-Dataset/bot_iot_balanced_subset_300k.csv"
df_original = pd.read_csv(data_path, low_memory=False)

pred_path = "/Users/nawara/Desktop/LLM-Clustering-Paper/Data/baseline_test_predictions.csv"
df_predictions = pd.read_csv(pred_path)

print("2. Selecting top 5,000 anomalies...")
top_k = 5000
test_preds_sorted = df_predictions.sort_values('lof_score', ascending=False)
top_anomalies_idx = test_preds_sorted.head(top_k).index
top_anomalies_features = df_original.loc[top_anomalies_idx].copy()
top_anomalies_scores = test_preds_sorted.head(top_k)[['lof_score', 'lof_pred', 'iso_forest_score', 'iso_forest_pred']].copy()
top_anomalies_data = pd.concat([top_anomalies_features.reset_index(drop=True), 
                                 top_anomalies_scores.reset_index(drop=True)], axis=1)

print("3. Preprocessing features...")
categorical_features = ['proto', 'state', 'saddr', 'sport', 'daddr', 'dport']
exclude_cols = categorical_features + ['lof_score', 'lof_pred', 'iso_forest_score', 'iso_forest_pred', 'attack', 'category', 'subcategory', 'pkSeqID']
numeric_features = top_anomalies_data.select_dtypes(include=[np.number]).columns.tolist()
numeric_features = [col for col in numeric_features if col not in exclude_cols]

full_data = pd.read_csv('/Users/nawara/Desktop/LLM-Clustering-Paper/Data/Bot-IoT-Dataset/bot_iot_balanced_subset_300k.csv')
X_train = full_data.sample(frac=0.7, random_state=42)

cat_encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1).fit(X_train[categorical_features])
num_scaler = StandardScaler().fit(X_train[numeric_features].astype(float))

X_anomalies_cat = cat_encoder.transform(top_anomalies_data[categorical_features])
X_anomalies_num = num_scaler.transform(top_anomalies_data[numeric_features].astype(float))
X_anomalies_scaled = np.hstack([X_anomalies_num, X_anomalies_cat])

print("4. Training K-Means with 3 clusters...")
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_anomalies_scaled)

unique_kmeans, counts_kmeans = np.unique(kmeans_labels, return_counts=True)
print(f"\nK-Means Cluster Distribution:")
for cluster_id, count in zip(unique_kmeans, counts_kmeans):
    pct = count / len(kmeans_labels) * 100
    print(f"  Cluster {cluster_id}: {count:,} samples ({pct:.1f}%)")

print("\n5. Applying PCA for 3D projection...")
pca_kmeans = PCA(n_components=3, random_state=42)
X_pca_kmeans = pca_kmeans.fit_transform(X_anomalies_scaled)

explained_var = pca_kmeans.explained_variance_ratio_
print(f"Explained variance (PC1, PC2, PC3): {explained_var[0]:.4f}, {explained_var[1]:.4f}, {explained_var[2]:.4f}")
print(f"Total variance captured: {explained_var.sum():.4f}")

print("\n6. Creating 3D visualization...")
fig = plt.figure(figsize=(16, 6))

# 3D scatter
ax1 = fig.add_subplot(121, projection='3d')
scatter = ax1.scatter(X_pca_kmeans[:, 0], X_pca_kmeans[:, 1], X_pca_kmeans[:, 2],
                     c=kmeans_labels, cmap='Set1', alpha=0.7, s=40, edgecolors='black', linewidth=0.3)
ax1.set_xlabel(f'PC1 ({explained_var[0]:.1%})', fontsize=11, fontweight='bold')
ax1.set_ylabel(f'PC2 ({explained_var[1]:.1%})', fontsize=11, fontweight='bold')
ax1.set_zlabel(f'PC3 ({explained_var[2]:.1%})', fontsize=11, fontweight='bold')
ax1.set_title('K-Means: 3D PCA Projection (All 5,000 Anomalies)\n3 Clusters - Clear Separation', 
             fontsize=13, fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax1, label='Cluster ID', shrink=0.8, pad=0.1)
ax1.view_init(elev=20, azim=45)
ax1.grid(True, alpha=0.3)

# Distribution chart
ax2 = fig.add_subplot(122)
colors_list = ['#FF6B6B', '#4ECDC4', '#FFE66D']
cluster_labels = [f'Cluster {i}' for i in range(3)]
bars = ax2.bar(cluster_labels, counts_kmeans, color=colors_list, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Number of Samples', fontsize=12, fontweight='bold')
ax2.set_title('K-Means Cluster Distribution\n(5,000 anomalies)', fontsize=13, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

for i, (bar, count) in enumerate(zip(bars, counts_kmeans)):
    pct = count / len(kmeans_labels) * 100
    ax2.text(i, count + 500, f'{count:,}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
output_path = '/Users/nawara/Desktop/LLM-Clustering-Paper/Data/kmeans_3d_pca_projection.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n✅ Visualization saved: Data/kmeans_3d_pca_projection.png")

print("\n" + "=" * 80)
print("K-Means 3D Visualization Complete!")
print("=" * 80)
