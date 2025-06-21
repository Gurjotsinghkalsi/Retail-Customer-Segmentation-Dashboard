# ml/update_segments.py

import pandas as pd
from sqlalchemy import create_engine, text

# 1. Connect to PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5433/postgres")

# 2. Load cluster data
df = pd.read_csv("clustered_customers.csv")

# 3. Map cluster numbers to segment names
cluster_to_segment = {
    0: "Average Buyers",
    1: "Top Spenders",
    2: "High Engagement",
    3: "Bulk One-Timers"
}

df['segment'] = df['cluster'].map(cluster_to_segment)

# 4. Ensure segment column exists in dim_customer
with engine.begin() as conn:
    conn.execute(text("""
        ALTER TABLE dim_customer
        ADD COLUMN IF NOT EXISTS segment TEXT;
    """))

# 5. Update dim_customer with segment for each customer
with engine.begin() as conn:
    for _, row in df.iterrows():
        conn.execute(
            text("UPDATE dim_customer SET segment = :segment WHERE customer_id = :customer_id"),
            {"segment": row["segment"], "customer_id": int(row["customer_id"])}
        )

print("✅ dim_customer table updated with segment labels.")