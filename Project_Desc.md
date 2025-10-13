# 🧠 Project_Desc.md — Personal Notes for "New Zealand Housing & Rental Analytics"

> **Purpose:** This document is my internal record of how the NZ Rental Analytics project was designed, what I learned, and how it can be extended in the future.

---

## 1. 🎯 Project Purpose

The goal of this project was to build a **complete, realistic SQL analytics pipeline** from scratch — something that looks like a real-world data warehouse and can showcase **data modelling, SQL querying, and Python integration** skills.

The dataset simulates **New Zealand housing rental prices**, reflecting:
- **Regional differences** (Auckland, Wellington, Christchurch)
- **Property types** (1–3 bedrooms)
- **Seasonality** (summer peaks, winter lows)
- **Gradual upward trend** and **realistic noise**

This project serves three main purposes:
1. **Portfolio piece** — to demonstrate SQL and data analytics capability.
2. **Learning framework** — to understand dimensional modelling and ETL patterns.
3. **Foundation for future products** — such as dashboards or a full-stack web demo.

---

## 2. 🧩 Data & Schema Design

### a. Data Model
- **Schema type:** Dimensional (Star Schema)
- **Core fact table:** `fact_rent`
- **Dimension tables:**
  - `dim_time` → month, year, quarter
  - `dim_suburb` → suburb, region, latitude, longitude
  - `dim_property_type` → 1/2/3-bedroom

Each row in `fact_rent` = one observation of  
→ (`time_id`, `suburb_id`, `property_type_id`) + (`median_rent`, `count_bonds`)

### b. Why Star Schema?
- Mirrors how BI/data warehouses model business data.
- Easy to query with joins and aggregate functions.
- Supports incremental updates (new months or new regions).
- Readability and explainability for interviews.

### c. ETL Flow
```

Raw CSV → staging (stg_rent)
→ dimensions (dim_time, dim_suburb, dim_property_type)
→ fact (fact_rent)

```
- All inserts are **idempotent** (`ON DUPLICATE KEY UPDATE`).
- Joins are **normalised** with `TRIM()` and `NULLIF()` to avoid join mismatch.
- The pipeline can be re-run safely any time.

---

## 3. ⚙️ Environment Setup

- **MySQL 8** (locally via Homebrew on macOS)
- **Python (Conda env)** with:
```

pandas, sqlalchemy, mysql-connector-python,
python-dotenv, matplotlib, jupyter

```
- `.env` file for DB credentials.
- Folder structure:
```

data/       (staging + processed)
sql/        (schema + load scripts)
notebooks/  (analysis, ETL, visualisation)
reports/    (figures + markdown)

```

---

## 4. 🔍 Core Analysis Logic

1. **Regional Trendline**  
 Average median rent by month, comparing Auckland, Wellington, and Christchurch.

2. **Month-over-Month (MoM) Change**  
 Using `LAG()` window function to calculate relative growth per suburb/type.

3. **Top Gainers (Latest Month)**  
 Ranking suburbs with highest MoM increase in rent.

4. **Rolling Volatility (3-Month)**  
 Short-term variability in rents using `STDDEV_SAMP()` window.

5. **Seasonality Profile**  
 Average rent by month-of-year to verify NZ summer/winter rental cycles.

6. **Region × Property Type Comparison**  
 Clustered bar chart for latest month snapshot.

---

## 5. 📊 Visual Outputs (Saved in `reports/figures/`)

| Figure | Description |
|:--|:--|
| `trend_auckland.png` | Auckland monthly rent trend |
| `regional_trend.png` | Multi-region rent comparison |
| `seasonality_by_region.png` | Seasonal profile per region |
| `top_mom_gainers.png` | Top month-over-month gainers |
| `latest_region_property_type.png` | Region × Property Type comparison |

---

## 6. 🧠 Key Learnings

### SQL Modelling
- Star schema is intuitive yet powerful for analytical workloads.
- Use surrogate keys and controlled joins to avoid duplication.
- CTEs and window functions make analytics declarative.

### ETL Best Practices
- Always **truncate staging** before reload.
- Idempotent inserts avoid duplicate facts.
- Normalise string fields before join (`TRIM`, `NULLIF`).

### Python Integration
- SQLAlchemy makes it easy to execute complex SQL while keeping flexibility.
- Pandas is great for post-query validation or visualisation.
- Always save outputs (`.csv`, `.png`) — reproducibility matters.

### Analytics
- MoM and rolling metrics show short-term dynamics.
- Seasonal decomposition can be extended with statsmodels later.
- Visualisation should remain minimal and clean (1 insight per chart).

---

## 7. 🚀 Possible Extensions

### 1. Web / Dashboard
- Build a simple **Flask** or **FastAPI** backend.
- Expose APIs like `/api/rent-trend?region=Auckland`.
- Use a frontend (React, Svelte, or plain HTML+Chart.js) to visualise trends dynamically.

### 2. Machine Learning
- Predict next 3 months’ rent by region using regression on time & property type.
- Add a `dim_economy` or `dim_inflation` table to enrich with macroeconomic data.

### 3. Spatial Analysis
- Use `lat/lon` to map suburbs on an interactive NZ map (e.g., Folium or Plotly).
- Could integrate with Google Maps API to geocode new suburbs.

### 4. BI Tools Integration
- Load the schema into **Power BI**, **Tableau**, or **Metabase**.
- Connect via MySQL connector and reuse SQL views as data sources.

### 5. Data Pipeline Automation
- Turn the ETL into an Airflow DAG or Prefect flow.
- Schedule monthly refresh with automated reporting.

---

## 8. 🗣️ Reflection

> Building this project taught me the full lifecycle of a small analytics system:
> - how to design a schema,
> - clean and load data safely,
> - write performant analytical SQL,
> - and present findings clearly.

It also gave me confidence to build **data products from scratch** and connect backend logic (SQL + Python) to visual dashboards.

If I ever turn this into a **web app**, it could become something like:
> *“New Zealand Rent Insights” — an interactive dashboard to track rent trends, compare regions, and forecast housing costs.*

---

## 9. 🧾 Maintenance Notes

- **Last data version:** `staging_rent.csv` (v3, 50 rows, 3 regions × 3 property types × Jan–Oct 2024)
- **Notebook:** `rental_insights.ipynb`
- **Python env:** `conda activate sql_project`
- **DB user:** `nz_user`
- **DB name:** `nz_rent`

To rebuild from scratch:
1. `DROP DATABASE nz_rent;`
2. Run schema SQL.
3. Recreate `.env` file.
4. Run notebook start-to-finish.

---

## 10. 🔗 Useful References
- Stats NZ Rental Market Dataset (for structure inspiration)  
- MBIE Tenancy Bond Data  
- Kimball & Ross – *The Data Warehouse Toolkit* (Star Schema design patterns)  
- SQL Window Functions guide – MySQL 8 documentation  

---

© 2025 — Personal notes by Minh Quach  
Project: *New Zealand Housing & Rental Analytics*  