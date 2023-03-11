'''
Tyrell Garza, Kevin Fu, Katie Vuong
Data Breach Analysis: Investigating Trends and Impact on Businesses

'''
import pandas as pd
from datetime import datetime
from dateutil import relativedelta
from typing import Tuple


# research question 1
def filter_by_year(
        data: pd.DataFrame, start_year: int, end_year: int
) -> pd.DataFrame:
    '''

    Vaidates accuracy/consistency data for question 1. Takes
    dataframe and two integer arguements, filters dataframe
    by year, returns resulting dataframe. (ensures data from
    desired years).
    '''
    return data[data['year'].between(start_year, end_year)]


def count_breaches_by_year(data: pd.DataFrame) -> Tuple[int, int]:
    '''

    Helps prove breach trend is increasing by calculating the
    number of breaches in the earliest and latest year
    of the dataset. See test for results.
    '''
    earliest_year = data['year'].min()
    latest_year = data['year'].max()
    breaches_in_earliest_year = data[data['year'] == earliest_year].shape[0]
    breaches_in_latest_year = data[data['year'] == latest_year].shape[0]
    return (breaches_in_earliest_year, breaches_in_latest_year)


# research question 3
def clean_dates(data: pd.DataFrame) -> pd.DataFrame:
    response_date = []

    # 365.25 days accounts for leap years which happen every 4 years,
    # 1/4 of 12 = .25
    average_days = 365.25 / 12

    # Apply string manipulation to match datetime format
    data["Date_Posted_or_Updated"] = (data[
                                      "Date_Posted_or_Updated"
                                      ].str.replace("-", "/"))
    data["breach_start"] = data["breach_start"].str.replace("-", "/")

    # Loop through end (d) and (b) start dates in pairs
    for d, b in zip(data["Date_Posted_or_Updated"], data["breach_start"]):

        # Create datetime objects to apply relativedelta function
        start = datetime.strptime(b, '%Y/%m/%d')
        end = datetime.strptime(d, '%Y/%m/%d')

        # Create relativedelta object to calculate exact time passed
        delta = relativedelta.relativedelta(end, start)
        print(delta.months + (delta.years * 12) + (delta.days / average_days))
        response_date.append(delta.months + (delta.years * 12) +
                                            (delta.days / average_days))
    data["response_time"] = pd.Series(response_date)
    return data


# research question 4
def clean_entities(data: pd.DataFrame) -> dict[str, int]:
    unique = {}
    breach_info = (data["Location_of_Breached_Information"].str.split(","))
    for i in breach_info:
        for j in i:
            j = j.strip()
            if j not in unique:
                unique[j] = 1
            else:
                unique[j] += 1
    return unique


# research question 5
def split_by_comma(data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    '''

    Takes dataframe and column name as arguements. Splits column
    values, creates new column, explodes into seperate rows and
    returns resulting dataframe. Ensures accuracy of "Type of Breach'
    values.
    '''
    return (
        data.assign(**{col_name: data[col_name].str.split(', ')}).
        explode(col_name)
    )


def total_individuals_affected(data: pd.DataFrame) -> pd.Series:
    '''

    Takes dataframe, returns series with total num of individuals
    affected by each type of breach sorted in descending order.
    Proving results of breach_individual_correlation. 
    '''
    return data.groupby(
                        'Type_of_Breach'
                        )[
                          'Individuals_Affected'
                          ].sum().sort_values(ascending=False)


def total_records_by_breach_type(data: pd.DataFrame) -> pd.Series:
    '''
    Takes dataframe, returns series with total num of records
    for each type of breach sorted in descending order.
    '''
    return data.groupby('Type of breach')['Total Records'].sum().sort_values(
        ascending=False)
