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


def file_name_contains_a_valid_time_interval(file_name, time_intervals):
    pattern = r'\d{4}'
    match = re.search(pattern, file_name)
    if match:
        time_interval_match = match.group()
        if time_interval_match in time_intervals:
            return time_interval_match
    else:
        return False


def extract_time_interval_dataframes(folder_path, time_intervals, sheet_name=None):
    files_by_time_interval = {}
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        time_interval_result = file_name_contains_a_valid_time_interval(file_name=file_name, time_intervals=time_intervals)
        if time_interval_result:
            file_path = os.path.join(folder_path, file_name)
            files_by_time_interval[time_interval_result] = extract_dataframe(file_path, sheet_name)
    return files_by_time_interval
