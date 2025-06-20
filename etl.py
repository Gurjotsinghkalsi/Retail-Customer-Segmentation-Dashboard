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

# ========== 5. Load fact_sales ==========

# Prepare base dataframe
sales_df = df[['InvoiceNo', 'CustomerID', 'StockCode', 'InvoiceDate', 'Quantity', 'UnitPrice']].dropna()

# Clean & rename columns
sales_df = sales_df.rename(columns={
    'InvoiceNo': 'invoice_no',
    'CustomerID': 'customer_id',
    'StockCode': 'product_id',
    'InvoiceDate': 'full_date',
    'Quantity': 'quantity',
    'UnitPrice': 'unit_price'
})
sales_df['full_date'] = pd.to_datetime(sales_df['full_date']).dt.date
sales_df['total_amount'] = sales_df['quantity'] * sales_df['unit_price']

# Load lookup tables
dim_date = pd.read_sql("SELECT date_id, full_date FROM dim_date", engine)
dim_product = pd.read_sql("SELECT product_id FROM dim_product", engine)
dim_customer = pd.read_sql("SELECT customer_id FROM dim_customer", engine)

# Merge to get foreign keys
sales_df = sales_df.merge(dim_date, how='left', on='full_date')
sales_df = sales_df.merge(dim_customer, how='inner', on='customer_id')
sales_df = sales_df.merge(dim_product, how='inner', on='product_id')

# Select required columns
fact_df = sales_df[['invoice_no', 'date_id', 'customer_id', 'product_id', 'quantity', 'unit_price', 'total_amount']].drop_duplicates()

with engine.begin() as conn:
    for _, row in fact_df.iterrows():
        conn.execute(text("""
            INSERT INTO fact_sales (invoice_no, date_id, customer_id, product_id, quantity, unit_price, total_amount)
            VALUES (:inv, :did, :cid, :pid, :qty, :price, :total)
            ON CONFLICT DO NOTHING
        """), {
            "inv": row['invoice_no'],
            "did": int(row['date_id']),
            "cid": int(row['customer_id']),
            "pid": row['product_id'],
            "qty": int(row['quantity']),
            "price": float(row['unit_price']),
            "total": float(row['total_amount'])
        })

print("✅ fact_sales populated (with UPSERT).")