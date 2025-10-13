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


sql = """
USE nz_rent;

-- dim_time
INSERT INTO dim_time (date_month, year, quarter, month)
SELECT DISTINCT date_month, YEAR(date_month), QUARTER(date_month), MONTH(date_month)
FROM stg_rent WHERE date_month IS NOT NULL
ON DUPLICATE KEY UPDATE date_month = VALUES(date_month);

-- dim_suburb
INSERT INTO dim_suburb (suburb_name, territorial_authority, region, suburb_code, lat, lon)
SELECT DISTINCT TRIM(suburb_name), NULLIF(TRIM(territorial_authority), ''), NULLIF(TRIM(region), ''), NULL, NULLIF(lat,0.0), NULLIF(lon,0.0)
FROM stg_rent WHERE suburb_name IS NOT NULL
ON DUPLICATE KEY UPDATE region=VALUES(region), territorial_authority=VALUES(territorial_authority);

-- dim_property_type
INSERT INTO dim_property_type (property_type_name)
SELECT DISTINCT TRIM(property_type) FROM stg_rent WHERE property_type IS NOT NULL
ON DUPLICATE KEY UPDATE property_type_name=VALUES(property_type_name);

-- fact_rent
INSERT INTO fact_rent (time_id, suburb_id, property_type_id, median_rent, count_bonds)
SELECT t.time_id, s.suburb_id, p.property_type_id, r.median_rent, r.count_bonds
FROM stg_rent r
JOIN dim_time t ON t.date_month = r.date_month
JOIN dim_suburb s ON s.suburb_name = r.suburb_name AND (s.region <=> r.region)
JOIN dim_property_type p ON p.property_type_name = r.property_type;
"""
with engine.begin() as conn:
    for stmt in sql.split(";"):
        if stmt.strip():
            conn.execute(text(stmt))

with engine.connect() as conn:
    total = conn.execute(text("SELECT COUNT(*) FROM fact_rent")).scalar()
    print("Rows in fact_rent:", total)