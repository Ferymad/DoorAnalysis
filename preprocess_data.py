import pandas as pd
import numpy as np

def preprocess_data(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    print(f"Original DataFrame shape: {df.shape}")
    print("First few rows of original data:")
    print(df.head())

    # Rename columns
    column_names = [
        'Unnamed: 0', 'start_date', 'end_date', 'code', 'color', 'model',
        '100cm', '100cm_glass', '90cm', '90cm_glass',
        'child_wing_closed', 'child_wing_open', 'frame', 'trim'
    ]

    # Ensure the number of column names matches the number of columns in the DataFrame
    if len(column_names) != len(df.columns):
        print(f"Warning: Number of columns in DataFrame ({len(df.columns)}) "
              f"doesn't match the number of column names ({len(column_names)})")
        # Use the original column names if there's a mismatch
        column_names = df.columns.tolist()

    df.columns = column_names

    # Convert date columns to datetime
    date_columns = ['start_date', 'end_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Identify numeric columns
    numeric_columns = ['100cm', '100cm_glass', '90cm', '90cm_glass', 'child_wing_closed', 'child_wing_open', 'frame', 'trim']
    
    # Convert numeric columns to float, replacing non-numeric values with NaN
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing values in numeric columns
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Create a unique identifier for each product combination
    id_columns = ['code', 'color', 'model']
    df['product_id'] = df[id_columns].astype(str).agg('_'.join, axis=1)

    # Calculate total sales for each row
    df['total_sales'] = df[numeric_columns].sum(axis=1)

    print(f"DataFrame shape after processing: {df.shape}")
    print("Sample of processed data:")
    print(df.head())

    # Remove rows where all sales columns are zero
    df = df[df['total_sales'] > 0]

    # Sort the dataframe by date and product_id
    df = df.sort_values(['start_date', 'product_id'])

    # Reset the index
    df = df.reset_index(drop=True)

    # Save the cleaned data to a new CSV file
    df.to_csv(output_csv, index=False)
    print(f"Preprocessed data saved to: {output_csv}")

    return df

if __name__ == "__main__":
    input_csv = "holydoor_sales_data.csv"
    output_csv = "holydoor_sales_data_cleaned.csv"
    
    cleaned_df = preprocess_data(input_csv, output_csv)
    
    # Display some basic information about the cleaned dataset
    print("\nDataset Information:")
    print(cleaned_df.info())
    
    print("\nSample of cleaned data:")
    print(cleaned_df.head())

    print("\nUnique products:")
    print(cleaned_df['product_id'].nunique())

    print("\nDate range:")
    print(f"Start: {cleaned_df['start_date'].min()}")
    print(f"End: {cleaned_df['end_date'].max()}")

    print("\nTotal sales summary:")
    print(cleaned_df['total_sales'].describe())