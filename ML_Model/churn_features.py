# ml_model/churn_features.py

import pandas as pd
from datetime import datetime

# Load the clustered customer data
clustered_df = pd.read_csv("clustered_customers.csv")

# Load original retail transactions
sales_df = pd.read_csv("../data/online_retail.csv")
sales_df["InvoiceDate"] = pd.to_datetime(sales_df["InvoiceDate"])

# Normalize column names for both DataFrames
clustered_df.columns = clustered_df.columns.str.lower()
sales_df.columns = sales_df.columns.str.lower()

# Step 1: Get last purchase date per customer
last_purchase = (
    sales_df.groupby("customerid")["invoicedate"]
    .max()
    .reset_index()
    .rename(columns={"invoicedate": "last_purchase_date"})
)

# print("Clustered DF Columns:", clustered_df.columns.tolist())
# print("Last Purchase DF Columns:", last_purchase.columns.tolist())

# Step 2: Days since last purchase (reference = most recent date in dataset)
latest_date = sales_df["invoicedate"].max()
last_purchase["days_since_last_purchase"] = (
    latest_date - last_purchase["last_purchase_date"]
).dt.days

# Step 3: Label customers as churned if inactive for 180+ days
last_purchase["is_churned"] = (last_purchase["days_since_last_purchase"] > 180).astype(int)

# Step 4: Merge churn info with original customer segments
df = pd.merge(clustered_df, last_purchase, left_on="customer_id", right_on="customerid", how="left")

# Step 5: Export final labeled dataset for model training
df.to_csv("../data/churn_labeled_customers.csv", index=False)
print("✅ Churn-labeled dataset saved to: ../data/churn_labeled_customers.csv")
