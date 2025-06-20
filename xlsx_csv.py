import pandas as pd

# Read Excel file
df = pd.read_excel('data/Online Retail.xlsx', engine='openpyxl')

# Save as CSV
df.to_csv('data/online_retail.csv', index=False)

print("✅ File converted to CSV successfully.")