import pandas as pd
import numpy as np
from src.tools.utils import get_firebase_data, data_to_df


def separate_data_by_month(df):
    """
    Separates given data by month and stores each month's data in a separate dictionary.

    Parameters
    ---------
    df : DataFrame
        Input dataframe which has a 'date' column. 'date' column can be in any format, it will be
        converted to datetime.

    Returns
    -------
    dict
        A dictionary where the keys are unique year-month pairs in the 'date' column of the
        input dataframe, and the values are dataframes containing all rows from the input
        dataframe that correspond to that year and month.
    """
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
    """
    Separate the data retrieved from Firebase by month and returns it.

    Functions
    ---------
    get_firebase_data :
         Retrieves data from Firebase.

    data_to_df :
         Transforms collected data into a DataFrame.

    separate_data_by_month :
         Splits the data into monthly periods.

    Returns
    -------
    DataFrame
        Returns the separated data by each month in a DataFrame.
    """
    data = get_firebase_data()
    df = data_to_df(data)
    separated = separate_data_by_month(df)
    return separated


def calculate_mean(df, data_type) -> float:
    """
    Calculates the mean value of measurements for a specific data type in a given DataFrame.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing the data to be processed. This DataFrame is expected to have at least two columns: 'dataType' and 'measurement'.

    data_type : str
        Category of data in the DataFrame for which the mean measurement is calculated.

    Returns
    -------
    float
        Returns the mean of measurements as a float value for the specified data type.
    """
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mean of the 'measurement' column
    mean_value = filtered_df['measurement'].mean()

    return float(mean_value)


def calculate_median(df, data_type) -> float:
    """
    Calculate and return the median value of the 'measurement' column for the specified data type from the given DataFrame.

    Parameters
    ---------
    df : pandas.DataFrame
        Dataframe which contains the data.

    data_type : str
        Type of data to calculate the median for. Function will filter the DataFrame for this data type.

    Returns
    -------
    float
        Median value of 'measurement' column for the specified data type.
    """
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the median of the 'measurement' column
    median_value = filtered_df['measurement'].median()

    return float(median_value)


def calculate_mode(df, data_type) -> pd.DataFrame:
    """
    Calculates the mode (most frequently occurring value) of the 'measurement' column in a DataFrame, for a specific data type.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to calculate mode.

    data_type : str
        Specific data type to filter DataFrame before calculating mode.

    Returns
    -------
    pd.Series
        Mode(s) of the 'measurement' column for the specific data type.
    """
    # Filter the DataFrame for the specified dataType
    filtered_df = df[df['dataType'] == data_type]

    # Calculate the mode of the 'measurement' column
    mode_values = filtered_df['measurement'].mode()

    return mode_values


def calculate_range(df, data_type) -> float:
    """
    Calculate the range of a particular type of data from a dataframe.

    Parameters
    ---------
    df : pandas dataframe
        The dataframe where the data is stored.

    data_type : str
        The type of data for which to calculate the range.

    Returns
    -------
    float
        The calculated range for the data type extracted from the dataframe.
    """
    selected_data = df[df['dataType'] == data_type]
    data_range = selected_data['measurement'].max() - selected_data['measurement'].min()
    return float(data_range)


def calculate_percentiles(df) -> pd.DataFrame:
    """
    Calculate and return the 25th, 50th, and 75th percentiles of measurements for each data type in a given DataFrame.

    Parameters
    ---------
    df : DataFrame
        A pandas DataFrame with at least two columns: 'dataType' and 'measurement'. The 'dataType'
        column categorizes each data point and 'measurement' is the numerical value of the data point.

    Returns
    -------
    DataFrame
        A new DataFrame where rows correspond to different 'dataType' and columns correspond to the
        requested percentiles: 0.25 (25th percentile), 0.5 (50th percentile or median), and 0.75
        (75th percentile).
    """
    percentiles = df.groupby('dataType')['measurement'].quantile([0.25, 0.5, 0.75]).unstack()
    return percentiles


def calculate_correlation(df) -> pd.Series:
    """
    Calculates the correlation between data types and measurements in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing data types and measurements.

    Returns
    -------
    pandas.Series
        Series representing the correlation between 'dataType' and 'measurement'.
    """
    correlation = df.groupby('dataType')['measurement'].corr()
    return correlation


def calculate_outliers(df, data_type):
    """
    Identify outliers in a dataframe for a specified data type based on z-score calculation.

    Parameters
    ---------
    df : DataFrame
        Input data in pandas DataFrame format.
    data_type : str, int, float
        The specific type of data on which the outlier detection will be executed.

    Returns
    -------
    DataFrame
        A DataFrame containing the outliers that were identified based on the z-score threshold.
    """
    target_df = df[df['dataType'] == data_type]

    # Calculate z-scores for the measurement column
    z_scores = np.abs((target_df['measurement'] - target_df['measurement'].mean()) / target_df['measurement'].std())

    # Define a threshold for outlier detection
    z_score_threshold = 3

    # Identify outliers based on the z-score threshold
    outliers = target_df[z_scores > z_score_threshold]
    return outliers
