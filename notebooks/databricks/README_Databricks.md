# NZ Housing & Rental Analytics – Databricks Edition (Azure, Standard Tier)

This is the **Databricks cloud version** of the NZ Rental Analytics project.  
It re-implements the original MySQL-based analytics pipeline using **Azure Databricks + Delta Lake**.

> Runs entirely on **Azure Databricks Standard Tier** (no SQL Warehouse required).

---

## Architecture Overview

```

Azure Storage (ADLS Gen2)
└── Container: nz-rent
├── bronze/      # raw CSV (staging_rent_*.csv)
├── silver/      # cleaned Delta
└── gold/        # Delta tables: dim_*, fact_rent, exports

Azure Databricks (Standard tier)
└── notebooks/databricks/
├── 00_mount_adls_gen2.py       # configure SAS, access ADLS, verify bronze
├── 01_silver_cleaning.py       # Bronze→Silver cleaning, Gold dims & fact build
├── 02_analytics_queries.py     # analysis (trend, MoM, volatility) + matplotlib dashboard
└── README_Databricks.md        # documentation (this file)

````

---

## Notebook Summary

| Notebook | Purpose | Key Outputs |
|-----------|----------|--------------|
| **00_mount_adls_gen2** | Configure Spark access to ADLS using SAS Token. Create and verify `/bronze` folder. | Connection test, sanity file |
| **01_silver_cleaning** | Perform full ETL: Bronze→Silver cleaning, build `dim_time`, `dim_suburb`, `dim_property_type`, and `fact_rent`. | Delta tables under `/silver` and `/gold` |
| **02_analytics_queries** | Execute analytical queries and visualise results with matplotlib. | PNG charts under `/FileStore/reports/` |

---

## Storage Access via SAS Token

In Azure Storage → **Shared access signature (SAS)**:
- Services: Blob
- Resource types: Container, Object
- Permissions: Read, Write, List
- Expiry: a few weeks

```python
# Inside 00_mount_adls_gen2.py
storage_account = "stnzrentdev"
container = "nz-rent"
account_fqdn = f"{storage_account}.dfs.core.windows.net"
abfss_url = f"abfss://{container}@{account_fqdn}/"
sas_token = "<paste ?sv=...>"

spark.conf.set(
  f"fs.azure.sas.{container}.{storage_account}.dfs.core.windows.net",
  sas_token
)
````

---

## Data Flow

**Bronze → Silver → Gold**

| Layer      | Description                                                                    | Example Path                       |
| ---------- | ------------------------------------------------------------------------------ | ---------------------------------- |
| **Bronze** | Raw CSV uploaded manually (no cleaning).                                       | `/bronze/staging_rent_2024_v3.csv` |
| **Silver** | Trimmed, typed, enriched with year/quarter/month.                              | `/silver/staging_rent_delta/`      |
| **Gold**   | Dimensional model: `dim_time`, `dim_suburb`, `dim_property_type`, `fact_rent`. | `/gold/dim_time/` etc.             |

Fact table grain = *(time_id, suburb_id, property_type_id)*
Measures = *median_rent, count_bonds*

---

## Analytics & Visualisation

Executed in `02_analytics_queries.py`:

* **Trendline**: average rent per region/month
* **Top MoM Gainers**: suburbs with highest month-over-month growth
* **Volatility**: 3-month rolling standard deviation

Each chart saved to:

```
/dbfs/FileStore/reports/trendline_region.png
/dbfs/FileStore/reports/top_mom_gainers.png
/dbfs/FileStore/reports/volatility.png
```

Accessible via:

```
https://<your-workspace>.azuredatabricks.net/files/reports/trendline_region.png
```

---

## Talking Points for Interview

* Built **end-to-end Lakehouse ETL** on Azure Databricks using Delta Lake.
* Designed a **Star Schema** with 3 dimensions and 1 fact table.
* Applied **Spark SQL window functions** for month-over-month and rolling analyses.
* Created a **notebook-native dashboard** (matplotlib) – cost-free alternative to Databricks SQL Warehouse.

---

## Future Improvements

* Automate monthly refresh via Databricks **Jobs**.
* Add **Great Expectations** for data quality checks in Silver.
* Deploy a **Streamlit** or **Power BI** dashboard reading from Gold exports.
* Explore **Forecasting (Prophet, Spark ML)** for rent prediction.

---

## Credits

Project built as part of the **Data Analytics Portfolio** to demonstrate:

* SQL → Spark migration,
* Lakehouse architecture (Bronze/Silver/Gold),
* Cloud-based visual analytics on Databricks.

© 2025 – Minh Quach
