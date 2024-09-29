import pandas as pd
import os

def convert_excel_to_csv(excel_path, csv_path, sheet_name='Satış'):
    # Check if the Excel file exists
    if not os.path.exists(excel_path):
        print(f"Error: The Excel file '{excel_path}' does not exist.")
        print("Current working directory:", os.getcwd())
        print("Files in current directory:", os.listdir())
        return

    try:
        # Read the Excel file
        df = pd.read_excel(excel_path, sheet_name=sheet_name, header=2, engine='openpyxl')
        
        # Save to CSV
        df.to_csv(csv_path, index=False)
        
        print(f"Conversion complete. CSV file saved to: {csv_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Pandas version:", pd.__version__)
        print("Openpyxl version:", pd.io.excel._openpyxl.__version__)

if __name__ == "__main__":
    # Get the current working directory
    current_dir = os.getcwd()
    
    # Use the new filename
    excel_filename = "data.xlsx"
    csv_filename = "holydoor_sales_data.csv"
    
    # Construct full paths
    excel_path = os.path.join(current_dir, excel_filename)
    csv_path = os.path.join(current_dir, csv_filename)
    
    # Print the full path of the Excel file for debugging
    print(f"Looking for Excel file at: {excel_path}")
    
    convert_excel_to_csv(excel_path, csv_path)