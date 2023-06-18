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


def calculate_mean(df, data_type) -> float:
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mean of the 'measurement' column
    mean_value = filtered_df['measurement'].mean()

    return float(mean_value)


def calculate_median(df, data_type) -> float:
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the median of the 'measurement' column
    median_value = filtered_df['measurement'].median()

    return float(median_value)


def calculate_mode(df, data_type) -> pd.DataFrame:
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mode of the 'measurement' column
    mode_values = filtered_df['measurement'].mode()

    return mode_values


def calculate_range(df, data_type) -> float:
    selected_data = df[df['dataType'] == data_type]
    data_range = selected_data['measurement'].max() - selected_data['measurement'].min()
    return float(data_range)


def calculate_percentiles(df) -> pd.DataFrame:
    percentiles = df.groupby('dataType')['measurement'].quantile([0.25, 0.5, 0.75]).unstack()
    return percentiles


def calculate_correlation(df) -> pd.Series:
    correlation = df.groupby('dataType')['measurement'].corr()
    return correlation


def calculate_outliers(df, data_type):
    target_df = df[df['dataType'] == data_type]

    # Calculate z-scores for the measurement column
    z_scores = np.abs((target_df['measurement'] - target_df['measurement'].mean()) / target_df['measurement'].std())

    # Define a threshold for outlier detection
    z_score_threshold = 3

    # Identify outliers based on the z-score threshold
    outliers = target_df[z_scores > z_score_threshold]
    return outliers




import requests

if __name__ == "__main__":
    # data = separate_data()
    response = requests.post(r"http://light-reality-293618.uc.r.appspot.com/api/chat_input",
                  data={
                      "input": "What was my heart rate on February 02?"
                  })
    pp().pprint(response.json())
    # pp().pprint(data["2023-02"])
    # print(calculate_outliers(data["2023-01"], data_type="waistCircumference"))
