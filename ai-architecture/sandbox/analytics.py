import pandas as pd
import numpy as np
from utils import get_firebase_data, data_to_df
from mapmaker import NestedMap
from pprint import PrettyPrinter as pp


def separate_data_by_month(df):
    # Convert date column to datetime if it's not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])

    # Create a dictionary to store the month-based dataframes
    month_dataframes = {}

    # Iterate over unique months in the dataframe
    for month in df['date'].dt.to_period('M').unique():
        # Filter the dataframe for each month and year
        month_df = df[(df['date'].dt.month == month.month) & (df['date'].dt.year == month.year)]

        # Store the month-based dataframe in the dictionary
        month_dataframes[str(month)] = month_df

    return month_dataframes


def separate_data():
    data = get_firebase_data()
    df = data_to_df(data)
    separated = separate_data_by_month(df)
    return separated


def calculate_mean(df, data_type):
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mean of the 'measurement' column
    mean_value = filtered_df['measurement'].mean()

    return mean_value


def calculate_median(df, data_type):
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the median of the 'measurement' column
    median_value = filtered_df['measurement'].median()

    return median_value


def calculate_mode(df, data_type):
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mode of the 'measurement' column
    mode_values = filtered_df['measurement'].mode()

    return mode_values


import requests

if __name__ == "__main__":
    # pp().pprint(separate_data())
    response = requests.post(r"http://127.0.0.1:5000//api/chat_input",
                  data={
                      "input": "Where is San Francisco?"
                  })
    pp().pprint(response.json())