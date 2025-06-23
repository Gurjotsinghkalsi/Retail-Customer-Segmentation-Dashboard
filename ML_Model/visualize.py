# visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Step 1: Load clustered data
df = pd.read_csv("clustered_customers.csv")

print(df.columns)
print(df.head())

# Step 2: Setup the plot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="total_revenue",
    y="avg_basket_size",
    hue="cluster",
    palette="tab10",
    s=100,
    edgecolor="black"
)

# Step 3: Add plot details
plt.title("Customer Segments Based on Revenue and Basket Size")
plt.xlabel("Total Revenue")
plt.ylabel("Average Basket Size")
plt.legend(title="Cluster")
plt.grid(True)

# Step 4: Save the plot (optional)
plt.tight_layout()
plt.savefig("customer_segments.png", dpi=300)

# Step 5: Show the plot
plt.show()