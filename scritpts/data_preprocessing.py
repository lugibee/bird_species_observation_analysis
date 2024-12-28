# data_preprocessing.py
import pandas as pd
import numpy as np
from scipy.stats import zscore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(forest_file, grassland_file):
    """
    Load all sheets from the forest and grassland Excel files and combine them into DataFrames.
    """
    logging.info("Loading data from forest and grassland files...")

    # Load all sheets from the forest file
    forest_sheets = pd.ExcelFile(forest_file).sheet_names
    forest_data = pd.concat(pd.read_excel(forest_file, sheet_name=sheet) for sheet in forest_sheets)
    forest_data['Location_Type'] = 'Forest'  # Add a column to identify forest data

    # Load all sheets from the grassland file
    grassland_sheets = pd.ExcelFile(grassland_file).sheet_names
    grassland_data = pd.concat(pd.read_excel(grassland_file, sheet_name=sheet) for sheet in grassland_sheets)
    grassland_data['Location_Type'] = 'Grassland'  # Add a column to identify grassland data

    logging.info("Data loading complete.")
    return forest_data, grassland_data

def handle_missing_values(data):
    """
    Handle missing values in the dataset.
    """
    logging.info("Handling missing values...")

    # Fill missing numerical values with median
    numerical_columns = ['temperature', 'humidity', 'distance', 'initial_three_min_cnt']
    for col in numerical_columns:
        if col in data.columns:
            data[col].fillna(data[col].median(), inplace=True)

    # Fill missing categorical values with "Unknown"
    categorical_columns = ['sex', 'id_method', 'sky', 'wind', 'disturbance', 'pif_watchlist_status', 'regional_stewardship_status']
    for col in categorical_columns:
        if col in data.columns:
            data[col].fillna("Unknown", inplace=True)

    # Fill missing dates with a placeholder (if necessary)
    if 'date' in data.columns:
        data['date'].fillna(pd.Timestamp("1900-01-01"), inplace=True)

    return data

def remove_outliers(data, column, threshold=3):
    """
    Remove outliers from a numerical column using z-score.
    """
    if column in data.columns:
        logging.info(f"Removing outliers from column: {column}")
        data = data[(np.abs(zscore(data[column].fillna(0))) < threshold)]
    return data

def remove_duplicates(data):
    """
    Remove duplicate records from the dataset.
    """
    logging.info("Removing duplicate records...")
    data.drop_duplicates(inplace=True)
    return data

def validate_data_types(data):
    """
    Ensure correct data types for columns.
    """
    logging.info("Validating and correcting data types...")

    # Convert numerical columns to numeric
    numerical_columns = ['temperature', 'humidity', 'distance', 'initial_three_min_cnt']
    for col in numerical_columns:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Convert boolean-like columns
    if 'flyover_observed' in data.columns:
        data['flyover_observed'] = data['flyover_observed'].astype(bool)

    # Convert date column to datetime
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

    return data

def clean_data(data):
    """
    Clean and preprocess the dataset.
    """
    logging.info("Cleaning data...")

    # Handle missing values
    data = handle_missing_values(data)

    # Remove duplicates
    data = remove_duplicates(data)

    # Remove outliers from specific columns
    for column in ['temperature', 'humidity', 'distance']:
        data = remove_outliers(data, column)

    # Validate and correct data types
    data = validate_data_types(data)

    # Extract Year and Month from Date
    if 'date' in data.columns:
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month

    # Standardize column names
    data.columns = data.columns.str.strip().str.replace(" ", "_").str.lower()

    logging.info("Data cleaning complete.")
    return data

def merge_datasets(forest_data, grassland_data):
    """
    Merge the forest and grassland datasets into a single DataFrame.
    """
    logging.info("Merging forest and grassland datasets...")

    # Align columns between the two datasets
    common_columns = list(set(forest_data.columns) & set(grassland_data.columns))
    forest_data = forest_data[common_columns]
    grassland_data = grassland_data[common_columns]

    # Merge the datasets
    combined_data = pd.concat([forest_data, grassland_data], ignore_index=True)

    logging.info("Datasets merged successfully.")
    return combined_data

def save_cleaned_data(data, output_path):
    """
    Save the cleaned dataset to a CSV file.
    """
    logging.info(f"Saving cleaned data to {output_path}...")
    data.to_csv(output_path, index=False)
    logging.info("Cleaned data saved successfully.")

if __name__ == "__main__":
    # File paths
    forest_file = "data\Bird_Monitoring_Data_FOREST.XLSX"
    grassland_file = "data\Bird_Monitoring_Data_GRASSLAND.XLSX"
    output_file = "data\cleaned_bird_data.csv"

    # Load, clean, and merge data
    logging.info("Starting data processing pipeline...")
    forest_data, grassland_data = load_data(forest_file, grassland_file)
    forest_data = clean_data(forest_data)
    grassland_data = clean_data(grassland_data)
    combined_data = merge_datasets(forest_data, grassland_data)
    save_cleaned_data(combined_data, output_file)

    logging.info("Data processing pipeline complete.")
