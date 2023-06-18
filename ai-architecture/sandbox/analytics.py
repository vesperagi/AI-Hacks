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


def get_mean(data_type: str):
    pass


if __name__ == "__main__":
    pp().pprint(separate_data())