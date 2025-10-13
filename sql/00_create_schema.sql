CREATE DATABASE IF NOT EXISTS nz_rent DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE nz_rent;

CREATE TABLE IF NOT EXISTS dim_time (
  time_id INT PRIMARY KEY AUTO_INCREMENT,
  date_month DATE NOT NULL,
  year SMALLINT NOT NULL,
  quarter TINYINT NOT NULL,
  month TINYINT NOT NULL,
  month_name VARCHAR(16) GENERATED ALWAYS AS (
    ELT(month, 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
  ) VIRTUAL,
  UNIQUE KEY uk_dim_time_date (date_month),
  KEY idx_dim_time_year_month (year, month)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_suburb (
  suburb_id INT PRIMARY KEY AUTO_INCREMENT,
  suburb_name VARCHAR(128) NOT NULL,
  territorial_authority VARCHAR(128),
  region VARCHAR(128),
  suburb_code VARCHAR(32),
  lat DECIMAL(9,6),
  lon DECIMAL(9,6),
  UNIQUE KEY uk_dim_suburb_name_region (suburb_name, region),
  KEY idx_dim_suburb_region (region)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dim_property_type (
  property_type_id TINYINT PRIMARY KEY AUTO_INCREMENT,
  property_type_name VARCHAR(64) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS fact_rent (
  rent_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  time_id INT NOT NULL,
  suburb_id INT NOT NULL,
  property_type_id TINYINT NOT NULL,
  median_rent DECIMAL(10,2) NOT NULL,
  count_bonds INT,
  CONSTRAINT fk_fact_time FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
  CONSTRAINT fk_fact_suburb FOREIGN KEY (suburb_id) REFERENCES dim_suburb(suburb_id),
  CONSTRAINT fk_fact_pt FOREIGN KEY (property_type_id) REFERENCES dim_property_type(property_type_id),
  UNIQUE KEY uk_fact (time_id, suburb_id, property_type_id),
  KEY idx_fact_suburb_time (suburb_id, time_id),
  KEY idx_fact_time (time_id),
  KEY idx_fact_pt (property_type_id)
) ENGINE=InnoDB;
