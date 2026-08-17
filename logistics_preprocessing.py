"""
Week 2 - Data Collection, Cleaning and Preprocessing
Logistics Data Analyst Intern

This script demonstrates a reproducible preprocessing pipeline:
1. Load raw logistics data
2. Inspect missing values and duplicates
3. Standardize categorical text
4. Convert numeric columns safely
5. Impute missing numeric values using the median
6. Detect and cap outliers using the IQR method
7. Normalize selected numerical variables using min-max scaling
8. Save the cleaned dataset
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "logistics_data_raw.csv"
CLEAN_FILE = BASE_DIR / "logistics_data_cleaned.csv"

NUMERIC_COLUMNS = [
    "distance_km",
    "delivery_time_min",
    "expected_time_min",
    "fuel_consumed_l",
    "transport_cost_inr",
]

NORMALIZE_COLUMNS = [
    "distance_km",
    "delivery_time_min",
    "transport_cost_inr",
]


def load_data(path=RAW_FILE):
    return pd.read_csv(path)


def inspect_data(df):
    print("\n--- SHAPE ---")
    print(df.shape)

    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)


def clean_text_columns(df):
    df = df.copy()
    df["vehicle_type"] = (
        df["vehicle_type"]
        .astype("string")
        .str.strip()
        .str.title()
    )
    return df


def convert_numeric_columns(df):
    df = df.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def remove_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def impute_missing_values(df):
    df = df.copy()
    for column in NUMERIC_COLUMNS:
        df[column] = df[column].fillna(df[column].median())
    return df


def cap_outliers_iqr(df, columns):
    """Cap extreme values to the IQR lower/upper bounds."""
    df = df.copy()
    bounds = {}

    for column in columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df[column] = df[column].clip(lower=lower, upper=upper)
        bounds[column] = (lower, upper)

    return df, bounds


def min_max_normalize(df, columns):
    """Create 0-1 normalized versions without replacing original values."""
    df = df.copy()

    for column in columns:
        min_value = df[column].min()
        max_value = df[column].max()

        if max_value != min_value:
            df[f"{column}_normalized"] = (
                (df[column] - min_value) / (max_value - min_value)
            )
        else:
            df[f"{column}_normalized"] = 0.0

    return df


def main():
    df = load_data()

    print("RAW DATA INSPECTION")
    inspect_data(df)

    # Step 1: standardize text
    df = clean_text_columns(df)

    # Step 2: safely convert numeric fields
    df = convert_numeric_columns(df)

    # Step 3: remove duplicate records
    before = len(df)
    df = remove_duplicates(df)
    print(f"\nDuplicates removed: {before - len(df)}")

    # Step 4: fill missing numeric values using medians
    missing_before = df[NUMERIC_COLUMNS].isna().sum().sum()
    df = impute_missing_values(df)
    print(f"Missing numeric values filled: {missing_before}")

    # Step 5: detect and cap extreme values
    df, bounds = cap_outliers_iqr(
        df,
        ["distance_km", "delivery_time_min", "transport_cost_inr"],
    )

    print("\nIQR OUTLIER BOUNDS")
    for column, (lower, upper) in bounds.items():
        print(f"{column}: {lower:.2f} to {upper:.2f}")

    # Step 6: normalize selected variables
    df = min_max_normalize(df, NORMALIZE_COLUMNS)

    # Final validation
    print("\n--- CLEANED DATA ---")
    print(df.head())

    print("\nRemaining missing values:")
    print(df.isna().sum().sum())

    print("\nRemaining duplicate rows:")
    print(df.duplicated().sum())

    df.to_csv(CLEAN_FILE, index=False)
    print(f"\nCleaned dataset saved to: {CLEAN_FILE}")


if __name__ == "__main__":
    main()
