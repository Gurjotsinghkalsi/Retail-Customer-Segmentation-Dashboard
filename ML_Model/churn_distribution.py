# churn_distribution.py

import pandas as pd
import matplotlib.pyplot as plt

# Load the labeled churn dataset
df = pd.read_csv("../data/churn_labeled_customers.csv")

# Count churn labels
churn_counts = df["is_churned"].value_counts().sort_index()
print("🔢 Churn Label Counts:\n", churn_counts)

# Optional percentage
percentages = churn_counts / churn_counts.sum() * 100
print("\n📊 Churn Percentage Breakdown:")
for label, pct in percentages.items():
    print(f"Class {label}: {pct:.2f}%")

# Plot the distribution
plt.bar(["Not Churned", "Churned"], churn_counts, color=["skyblue", "salmon"])
plt.title("Customer Churn Class Distribution")
plt.ylabel("Number of Customers")
plt.show()