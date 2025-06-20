import pandas as pd
from sqlalchemy import create_engine, text

# Connect to PostgreSQL
engine = create_engine("postgresql://postgres:admin@localhost:5433/postgres")

# Load the dataset
df = pd.read_csv("data/online_retail.csv")

# Clean the data
df = df.dropna(subset=['CustomerID', 'Country'])  # Essential fields

# ========== 1. Load dim_country ==========
country_df = pd.DataFrame(df['Country'].dropna().unique(), columns=['country_name'])

with engine.begin() as conn:
    for country in country_df['country_name']:
        conn.execute(text("""
            INSERT INTO dim_country (country_name)
            VALUES (:country)
            ON CONFLICT (country_name) DO NOTHING
        """), {"country": country})

print("✅ dim_country populated (with UPSERT).")

# ========== 2. Load dim_customer ==========
# Load dim_country into a DataFrame to get country_id
dim_country_df = pd.read_sql("SELECT * FROM dim_country", engine)

# Merge country_id into customer records
customer_df = df[['CustomerID', 'Country']].drop_duplicates()
customer_df = customer_df.merge(dim_country_df, how='left', left_on='Country', right_on='country_name')
customer_df = customer_df[['CustomerID', 'country_id']].rename(columns={
    'CustomerID': 'customer_id'
})

with engine.begin() as conn:
    for _, row in customer_df.iterrows():
        conn.execute(text("""
            INSERT INTO dim_customer (customer_id, country_id)
            VALUES (:cid, :ccid)
            ON CONFLICT (customer_id) DO NOTHING
        """), {
            "cid": int(row['customer_id']),
            "ccid": int(row['country_id'])
        })

print("✅ dim_customer populated (with UPSERT).")