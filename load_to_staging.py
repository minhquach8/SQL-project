import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

USER = os.getenv("MYSQL_USER")
PWD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("MYSQL_PORT")
DB = os.getenv("MYSQL_DB")

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

ddl = """
CREATE TABLE IF NOT EXISTS stg_rent (
  date_month DATE,
  suburb_name VARCHAR(128),
  region VARCHAR(128),
  territorial_authority VARCHAR(128),
  property_type VARCHAR(64),
  median_rent DECIMAL(10,2),
  count_bonds INT,
  lat DECIMAL(9,6),
  lon DECIMAL(9,6)
) ENGINE=InnoDB;
"""

with engine.begin() as conn:
  conn.execute(text("USE nz_rent;"))
  conn.execute(text(ddl))
  

df = pd.read_csv("data/staging/staging_rent.csv")
df['date_month'] = pd.to_datetime(df['date_month']).dt.date
df.to_sql('stg_rent', con=engine, if_exists='append', index=False)
print("Rows in staging:", pd.read_sql("SELECT COUNT(*) cnt FROM stg_rent;", engine).iloc[0, 0])