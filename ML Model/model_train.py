# ml/model_train.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Step 1: Load customer features
df = pd.read_csv("cluster_segments.csv")

# Save customer_id separately to reattach after scaling
customer_ids = df['customer_id']
X = df.drop(columns=['customer_id'])

# Step 2: Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Train KMeans model
k = 4  # Number of clusters (can tune this later)
kmeans = KMeans(n_clusters=k, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Step 4: Export cluster labels
# Save all features + cluster label + customer_id
df_full = pd.concat([customer_ids, pd.DataFrame(X, columns=X.columns)], axis=1)
df_full['cluster'] = df['cluster']
df_full.to_csv("clustered_customers.csv", index=False)

# Step 5: Summarize each cluster (mean metrics)
summary = df.groupby('cluster').mean(numeric_only=True)
print("📊 Cluster Summary:")
print(summary)

# Optional: Elbow method plot
inertia = []
k_range = range(1, 10)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(X_scaled)
    inertia.append(km.inertia_)

plt.plot(k_range, inertia, marker='o')
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.grid()
plt.show()

# cluster labelling 
print("📊 Cluster Summary:")
print(df.groupby('cluster').mean(numeric_only=True))