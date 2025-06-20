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

# ========== 3. Load dim_product ==========
# Clean: Drop rows with missing StockCode, Description, or UnitPrice
product_df = df[['StockCode', 'Description', 'UnitPrice']].dropna().drop_duplicates()
product_df = product_df.rename(columns={
    'StockCode': 'product_id',
    'Description': 'description',
    'UnitPrice': 'unit_price'
})

# Optional: Add placeholder 'category' column (can enhance later)
product_df['category'] = 'Unknown'

with engine.begin() as conn:
    for _, row in product_df.iterrows():
        conn.execute(text("""
            INSERT INTO dim_product (product_id, description, category, unit_price)
            VALUES (:pid, :desc, :cat, :price)
            ON CONFLICT (product_id) DO NOTHING
        """), {
            "pid": str(row['product_id']),
            "desc": str(row['description']),
            "cat": row['category'],
            "price": float(row['unit_price'])
        })

print("✅ dim_product populated (with UPSERT).")

# ========== 4. Load dim_date ==========
# Extract dates from InvoiceDate column
date_df = df[['InvoiceDate']].dropna().drop_duplicates()
date_df['full_date'] = pd.to_datetime(date_df['InvoiceDate']).dt.date

# Remove duplicates again, keep only date part
date_df = pd.DataFrame(date_df['full_date'].unique(), columns=['full_date'])

# Extract date parts
date_df['year'] = pd.to_datetime(date_df['full_date']).dt.year
date_df['month'] = pd.to_datetime(date_df['full_date']).dt.month
date_df['day'] = pd.to_datetime(date_df['full_date']).dt.day
date_df['weekday'] = pd.to_datetime(date_df['full_date']).dt.day_name()

with engine.begin() as conn:
    for _, row in date_df.iterrows():
        conn.execute(text("""
            INSERT INTO dim_date (full_date, year, month, day, weekday)
            VALUES (:date, :yr, :mon, :d, :wday)
            ON CONFLICT (full_date) DO NOTHING
        """), {
            "date": row['full_date'],
            "yr": int(row['year']),
            "mon": int(row['month']),
            "d": int(row['day']),
            "wday": row['weekday']
        })

print("✅ dim_date populated (with UPSERT).")