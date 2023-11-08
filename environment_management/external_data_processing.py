import os
import pandas as pd
import re


def combine_column_names(*args):
    column_names = []
    for arg in args:
        if isinstance(arg, str):
            column_names.append(arg)
        elif isinstance(arg, list):
            column_names.extend(arg)
    return column_names


def get_file_extension(file_path):
    file_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(file_name)
    return extension


def extract_dataframe(file_path, sheet_name=None):
    file_extension = get_file_extension(file_path)
    if file_extension in ['.xls', '.xlsx']:
        if sheet_name:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            return pd.read_excel(file_path)
    elif file_extension in ['.csv']:
        return pd.read_csv(file_path)
    else:
        raise Exception(f"File path {file_path} does not have one of valid extensions .csv, .xls, or .xlsx")


def extract_dataframe_by_columns(file_path, column_names, sheet_name=None):
    df = extract_dataframe(file_path=file_path,
                           sheet_name=sheet_name)
    return df[column_names]


def file_name_contains_a_valid_year(file_name, years):
    pattern = r'\d{4}'
    match = re.search(pattern, file_name)
    if match:
        year_match = match.group()
        if year_match in years:
            return year_match
    else:
        return False


def extract_year_dataframes(folder_path, years, sheet_name=None):
    files_by_year = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        year_result = file_name_contains_a_valid_year(file_name=file_name, years=years)
        if year_result:
            file_path = os.path.join(folder_path, file_name)
            files_by_year[year_result] = extract_dataframe(file_path, sheet_name)
    return files_by_year
