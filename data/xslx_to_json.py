"""
This module converts the dataset from the discord league in .xlsx file to a
.json file that will be used for training the NN
"""

import pandas as pd
import json


# Define Excel and JSON file path
EXCEL_FILE = 'tfm_ranked_dataset.xlsx'
JSON_FILE = 'data.json'


def generate_df(cols, given_sheet_name):
    df = pd.read_excel(EXCEL_FILE, usecols = cols, sheet_name = given_sheet_name)
    return df


def main():
    # Define names of columns to select
    character_columns = ['B1', 'B2', 'B3', 'B4', 'R1', 'R2', 'R3', 'R4']
    result_column = 'Winner'
    usecols = character_columns + [result_column]
    
    # Define what sheets to read through for data
    sheets = ['Patch3', 'Patch3.2']
    
    # Convert DataFrames to list of dicts
    data = []
    for sheet in sheets:
        # Read data from excel file into DataFrame
        df = generate_df(usecols, sheet)
        
        # Convert DataFrame into list of dicts
        for index, row in df.iterrows():
            if not row[usecols].isnull().any():
                entry = {
                    'characters': row[character_columns].tolist(),
                    'result': row[result_column]
                }
                data.append(entry)
    
    # Write data to JSON file
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, indent = 4)
    
    print(f'Data has been converted and saved to {JSON_FILE}.')


if __name__ == '__main__':
    main()