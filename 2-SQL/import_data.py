import pandas as pd
import sqlite3
df= pd.read_csv("1-dataset/credit_risk_dataset.csv")
conn=sqlite3.connect("2-sql/credit_risk.db")
df.to_sql(
    "credit_risk",
    conn,
    if_exists="replace",
    index=False
)
conn.close()
print("Data imported successfully")
