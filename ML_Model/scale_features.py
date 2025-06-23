# ml_model/scale_features.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the churn-labeled dataset
df = pd.read_csv("../data/churn_labeled_customers.csv")

# Select relevant numeric features
features = ["total_revenue", "avg_basket_size", "unique_products", "days_since_last_purchase"]
X = df[features]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Output: scaled features and labels
y = df["is_churned"]

# Save scaled features to CSV (optional, for inspection or reuse)
scaled_df = pd.DataFrame(X_scaled, columns=features)
scaled_df["is_churned"] = y
scaled_df.to_csv("../data/scaled_churn_data.csv", index=False)

print("✅ Scaled features saved to ../data/scaled_churn_data.csv")