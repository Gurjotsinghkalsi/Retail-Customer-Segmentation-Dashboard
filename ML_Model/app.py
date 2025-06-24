# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df = pd.read_csv("./clustered_customers.csv")

# Add segment labels
cluster_to_segment = {
    0: "Average Buyers",
    1: "Top Spenders",
    2: "High Engagement",
    3: "Bulk One-Timers"
}
df["segment"] = df["cluster"].map(cluster_to_segment)

# Page setup
st.set_page_config(page_title="Customer Segments", layout="wide")
st.title("🛍️ Retail Customer Intelligence Dashboard")

# --- Global Charts (Across All Segments) ---
st.subheader("📊 Customer Base Breakdown")

# Bar Chart: Customer Count per Segment
segment_counts = df['segment'].value_counts()
fig1, ax1 = plt.subplots(figsize=(6, 3))
segment_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_ylabel("Number of Customers")
ax1.set_xlabel("Segment")
ax1.set_title("Customer Distribution by Segment")
plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig1)

# Pie Chart: Revenue Share by Segment
revenue_by_segment = df.groupby("segment")["total_revenue"].sum().reset_index()
fig2 = px.pie(revenue_by_segment, values='total_revenue', names='segment',
              title='💰 Share of Revenue by Customer Segment', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- Segment Filter ---
st.subheader("🎯 Choose a Segment to Explore")
segment = st.selectbox("Select Segment", df["segment"].unique())
filtered = df[df["segment"] == segment]

# Segment-Level Stats
st.subheader(f"📈 Key Metrics: {segment} Segment")
col1, col2, col3 = st.columns(3)
col1.metric("Average Revenue per Customer", f"${filtered['total_revenue'].mean():,.2f}")
col2.metric("Average Transaction Value", f"{filtered['avg_basket_size'].mean():.2f}")
col3.metric("Avg. Product Variety per Customer", f"{filtered['unique_products'].mean():.0f}")

# Segment-Level Scatter Plot
st.subheader("🧺 Spending Pattern: Basket Size vs Revenue")
fig3 = px.scatter(
    filtered,
    x="avg_basket_size",
    y="total_revenue",
    color="segment",
    hover_data=["customer_id"],
    title=f"Basket Size vs Revenue — {segment}"
)
st.plotly_chart(fig3, use_container_width=True)

import joblib

# Load model and scaler
model = joblib.load("../data/churn_model.pkl")
scaler = joblib.load("../data/churn_scaler.pkl")

# Load churn labeled data
df_churn = pd.read_csv("../data/churn_labeled_customers.csv")

# Merge churn info and required features into original filtered data
churn_features = ["customer_id", "days_since_last_purchase", "is_churned"]
merged = pd.merge(filtered, df_churn[churn_features], on="customer_id", how="left")

# print(df.columns.tolist())

# print(df_churn.columns.tolist())

# Features used in training
features = ["total_revenue", "total_invoices", "avg_basket_size", "unique_products"]

# Predict churn on current segment
X = merged[features]
X_scaled = scaler.transform(X)
merged["churn_pred"] = model.predict(X_scaled)

# Show churn insight
st.subheader("📉 Churn Predictions")
churn_rate = merged["churn_pred"].mean()
st.metric("Predicted Churn Rate", f"{churn_rate*100:.2f}%")

# Pie chart visualization
churn_counts = merged["churn_pred"].value_counts().rename({0: "Active", 1: "Churned"})
fig = px.pie(
    names=churn_counts.index,
    values=churn_counts.values,
    title="🔍 Predicted Churn Distribution"
)
st.plotly_chart(fig)

# Show updated table
st.subheader("📋 Customers with Churn Prediction")
st.dataframe(merged.sort_values("total_revenue", ascending=False), use_container_width=True)

# CSV Download
st.download_button("Download Churn Data", merged.to_csv(index=False), file_name=f"{segment}_churn_customers.csv")

# Segment Customer Table
st.subheader(f"📋 Customer List: {segment} Segment")
st.dataframe(filtered.sort_values("total_revenue", ascending=False), use_container_width=True)

# Download Button
st.download_button(
    label="📥 Download Segment Data (CSV)",
    data=filtered.to_csv(index=False),
    file_name=f"{segment}_customers.csv"
)