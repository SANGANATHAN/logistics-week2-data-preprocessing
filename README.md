# Week 2 - Logistics Data Cleaning and Preprocessing

## Yuva Intern: Logistics Data Analyst Intern

### Task

**Week 2: Data Collection, Cleaning, and Preprocessing for Logistics Analysis**

## Project Overview

This project demonstrates a reproducible logistics data preprocessing pipeline using Python and Pandas. The pipeline simulates the preparation of delivery data for later analytics and machine-learning tasks.

The project uses a small representative dataset for demonstration. The dataset structure is inspired by publicly available supply-chain datasets such as the **DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS** dataset.

Public dataset reference:
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

The local raw CSV intentionally contains controlled data-quality problems so that the cleaning methods can be demonstrated clearly.

## Data Collection Simulation

A logistics dataset may be collected from order-management systems, warehouse records, GPS/route systems, vehicle logs, and delivery applications. Typical fields include order ID, date, origin, destination, vehicle type, distance, delivery time, expected time, fuel consumption, and transportation cost.

For this internship demonstration, a small sample CSV is used instead of copying a large external dataset.

## Data Quality Issues Simulated

The raw dataset contains:

- Missing numerical values.
- A duplicate record.
- Extreme values that act as outliers.
- Inconsistent text formatting in a vehicle-type field.
- Numerical fields that require explicit type validation.

## Cleaning Methodology

### 1. Missing Values

Missing numerical values are converted to proper numeric types and filled using the median. The median is less sensitive to extreme values than the mean and is therefore suitable for this demonstration.

### 2. Duplicate Records

Duplicate rows are removed because repeated transactions can incorrectly increase order counts and distort averages.

### 3. Text Standardization

Vehicle-type values are stripped of extra spaces and converted to title case so that values such as `van`, ` Van ` and `VAN` can be treated consistently.

### 4. Outlier Detection

The Interquartile Range (IQR) method is used. Values below `Q1 - 1.5 × IQR` or above `Q3 + 1.5 × IQR` are considered extreme. For this demonstration, extreme values are capped to the IQR boundaries instead of deleting the complete records.

### 5. Normalization

Min-max normalization converts selected numerical variables to a 0–1 scale:

`normalized = (x - minimum) / (maximum - minimum)`

This is useful when variables with different units and ranges are later used together in analytical or machine-learning models.

## Pipeline

```text
Raw Data
   ↓
Data Inspection
   ↓
Text Standardization
   ↓
Numeric Type Conversion
   ↓
Duplicate Removal
   ↓
Missing Value Imputation
   ↓
Outlier Detection and Capping
   ↓
Min-Max Normalization
   ↓
Validation
   ↓
Clean Dataset
```

## Files

- `logistics_data_raw.csv` – raw sample data with controlled quality issues.
- `logistics_preprocessing.py` – complete preprocessing script.
- `logistics_data_cleaned.csv` – generated after running the script.
- `requirements.txt` – required Python package.
- `README.md` – project documentation.

## How to Run

```bash
pip install -r requirements.txt
python logistics_preprocessing.py
```

The script creates `logistics_data_cleaned.csv` in the same folder.

## Expected Outcome

After preprocessing, the dataset should contain no missing numerical values or duplicate rows, categorical text should be consistent, extreme values should be controlled, and normalized columns should be available for subsequent analysis.

## Why Data Quality Matters

Logistics decisions depend on accurate delivery, cost, route, and fuel information. Poor-quality data can produce misleading KPIs, inaccurate predictions, and inefficient resource allocation. A systematic preprocessing pipeline improves the reliability of subsequent analysis and decision-making.

## Note

The local dataset is a synthetic educational sample. It does not contain real customer or company information.
