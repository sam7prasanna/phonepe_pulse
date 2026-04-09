-- DATABASE CREATION

CREATE DATABASE IF NOT EXISTS phonepe_data;
USE phonepe_data;

-- AGGREGATED TABLES

CREATE TABLE aggregated_transaction (
    state VARCHAR(100),
    year INT,
    quarter INT,
    txn_type VARCHAR(100),
    txn_count BIGINT,
    txn_amount DOUBLE
);

CREATE TABLE aggregated_user (
    state VARCHAR(100),
    year INT,
    quarter INT,
    device_brand VARCHAR(100),
    device_user_count BIGINT,
    total_registered_users BIGINT,
    total_app_opens BIGINT
);

CREATE TABLE aggregated_insurance (
    state VARCHAR(100),
    year INT,
    quarter INT,
    ins_count BIGINT,
    ins_amount DOUBLE
);

-- MAP TABLES

CREATE TABLE map_transaction (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    txn_count BIGINT,
    txn_amount DOUBLE
);

CREATE TABLE map_user (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    registered_users BIGINT,
    app_opens BIGINT
);

CREATE TABLE map_insurance (
    state VARCHAR(100),
    district VARCHAR(100),
    year INT,
    quarter INT,
    ins_count BIGINT,
    ins_amount DOUBLE
);

-- TOP TABLES

CREATE TABLE top_transaction (
    parent_state VARCHAR(100),
    entity_name VARCHAR(100),   -- district / pincode
    entity_type VARCHAR(50),    -- 'district' or 'pincode'
    year INT,
    quarter INT,
    txn_count BIGINT,
    txn_amount DOUBLE
);

CREATE TABLE top_user (
    parent_state VARCHAR(100),
    entity_name VARCHAR(100),
    entity_type VARCHAR(50),
    registered_users BIGINT
);

-- SCENARIO 1: TRANSACTION DYNAMICS

-- Yearly Transaction Trend
SELECT 
    year,
    SUM(txn_count)  AS total_txn_count,
    SUM(txn_amount) AS total_txn_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;

-- Transaction Type Trend
SELECT 
    year,
    txn_type,
    SUM(txn_count)  AS total_txn_count,
    SUM(txn_amount) AS total_txn_amount
FROM aggregated_transaction
GROUP BY year, txn_type
ORDER BY year, total_txn_amount DESC;

-- State-wise Transactions
SELECT 
    state,
    year,
    SUM(txn_count)  AS total_txn_count,
    SUM(txn_amount) AS total_txn_amount
FROM aggregated_transaction
GROUP BY state, year
ORDER BY year, total_txn_amount DESC;

-- SCENARIO 2: DEVICE DOMINANCE & ENGAGEMENT

-- Device Brand Trend
SELECT
    year,
    device_brand,
    SUM(device_user_count) AS total_registered_users
FROM aggregated_user
GROUP BY year, device_brand
ORDER BY year, total_registered_users DESC;

-- State-wise Device Usage
SELECT
    state,
    year,
    device_brand,
    SUM(device_user_count) AS total_users
FROM aggregated_user
GROUP BY state, year, device_brand;

-- Engagement Analysis
SELECT
    state,
    year,
    SUM(total_registered_users) AS total_registered_users,
    SUM(total_app_opens)       AS total_app_opens
FROM aggregated_user
WHERE total_registered_users IS NOT NULL
  AND total_app_opens IS NOT NULL
GROUP BY state, year;

-- SCENARIO 3: INSURANCE ANALYSIS

-- Yearly Insurance Growth
SELECT
    year,
    SUM(ins_count)  AS total_insurance_policies,
    SUM(ins_amount) AS total_insurance_value
FROM aggregated_insurance
GROUP BY year
ORDER BY year;

-- State-wise Insurance
SELECT
    state,
    year,
    SUM(ins_count)  AS total_insurance_policies,
    SUM(ins_amount) AS total_insurance_value
FROM aggregated_insurance
GROUP BY state, year
ORDER BY total_insurance_value DESC;

-- District-level Insurance
SELECT
    state,
    district,
    year,
    SUM(ins_count)  AS total_insance_policies,
    SUM(ins_amount) AS total_insurance_value
FROM map_insurance
GROUP BY state, district, year;

-- SCENARIO 4: MARKET EXPANSION

-- State-Year Transaction Summary
SELECT 
    state,
    year,
    SUM(txn_count)  AS total_txn_count,
    SUM(txn_amount) AS total_txn_amount
FROM aggregated_transaction
GROUP BY state, year
ORDER BY state, year;

-- Market Size by State
SELECT
    state,
    SUM(txn_count)  AS total_txn_count,
    SUM(txn_amount) AS total_txn_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_txn_amount DESC;

-- SCENARIO 5: USER ENGAGEMENT

-- State-wise User Base
SELECT
    state,
    SUM(registered_users) AS total_registered_users,
    SUM(app_opens)        AS total_app_opens
FROM map_user
GROUP BY state
ORDER BY total_registered_users DESC;

-- District-wise Engagement
SELECT
    state,
    district,
    SUM(registered_users) AS total_registered_users,
    SUM(app_opens)        AS total_app_opens
FROM map_user
GROUP BY state, district
ORDER BY total_registered_users DESC;

-- Top Pincode Registrations
SELECT
    parent_state AS state,
    entity_name  AS pincode,
    SUM(registered_users) AS total_registrations
FROM top_user
WHERE entity_type = 'pincode'
GROUP BY parent_state, entity_name
ORDER BY total_registrations DESC;

-- Top performing states/districts
SELECT 
    parent_state,
    entity_name,
    SUM(txn_amount) AS total_amount
FROM top_transaction
GROUP BY parent_state, entity_name
ORDER BY total_amount DESC; 