import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore

# Replace with your own password if changed
engine = create_engine('postgresql://postgres:admin@localhost:5433/postgres')

# Load CSV
df = pd.read_csv('data/online_retail.csv')

# Preview
print(df.head())

# Example: insert unique countries
countries = pd.DataFrame(df['Country'].dropna().unique(), columns=['country_name'])
countries.to_sql('dim_country', engine, if_exists='append', index=False)

# You’ll do similar logic for other tables (product, customer, sales)