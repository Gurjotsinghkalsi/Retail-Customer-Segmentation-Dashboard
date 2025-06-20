# features.py

import pandas as pd
from sqlalchemy import create_engine

# Step 1: Connect to your local PostgreSQL DB (adjust port if not 5432)
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5433/postgres")

# Step 2: Run SQL to extract and aggregate customer features
query = """
    SELECT 
        f.customer_id,
        SUM(f.total_amount) AS total_revenue,
        COUNT(DISTINCT f.invoice_no) AS total_invoices,
        SUM(f.quantity)::float / COUNT(DISTINCT f.invoice_no) AS avg_basket_size,
        COUNT(DISTINCT f.product_id) AS unique_products
    FROM fact_sales f
    WHERE f.customer_id IS NOT NULL
    GROUP BY f.customer_id
    ORDER BY f.customer_id;
"""

# Step 3: Load result into pandas DataFrame
df_features = pd.read_sql_query(query, engine)

# Step 4: Preview output
print(df_features.head())

# Optional: Save for modeling
df_features.to_csv("cluster_segments.csv", index=False)