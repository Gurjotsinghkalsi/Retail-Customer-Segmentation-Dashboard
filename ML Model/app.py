# ml/app.py

import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("clustered_customers.csv")

# Add segment labels (if not already in file)
cluster_to_segment = {
    0: "Average Buyers",
    1: "Top Spenders",
    2: "High Engagement",
    3: "Bulk One-Timers"
}
df["segment"] = df["cluster"].map(cluster_to_segment)

# Streamlit UI
st.set_page_config(page_title="Customer Segments", layout="wide")
st.title("🛍️ Customer Segment Explorer")

# Segment filter
segment = st.selectbox("Choose a Segment", df["segment"].unique())

# Filtered data
filtered = df[df["segment"] == segment]

# Show key stats
st.subheader("📊 Segment Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Revenue", f"${filtered['total_revenue'].mean():.2f}")
col2.metric("Avg. Basket Size", f"{filtered['avg_basket_size'].mean():.2f}")
col3.metric("Unique Products", f"{filtered['unique_products'].mean():.0f}")

# Show table
st.subheader("📋 Customers in Segment")
st.dataframe(filtered.sort_values("total_revenue", ascending=False), use_container_width=True)

# Optional download
st.download_button("Download CSV", filtered.to_csv(index=False), file_name=f"{segment}_customers.csv")