'''
Tyrell Garza, Kevin Fu, Katie Vuong
Data Breach Analysis: Investigating Trends and Impact on Businesses

'''
import pandas as pd
from datetime import datetime
from dateutil import relativedelta


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
