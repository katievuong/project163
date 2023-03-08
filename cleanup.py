import pandas as pd
from datetime import datetime
from dateutil import relativedelta


# research question 3
def clean_dates(data: pd.DataFrame) -> None:
    response_date = []
    thirty = ["04", "06", "09", "11"]
    thirty_one = ["01", "03", "05", "07", "08", "10", "12"]
    leap = ["2004", "2008", "2012", "2016"]
    data["Date_Posted_or_Updated"] = (data[
                                      "Date_Posted_or_Updated"
                                      ].str.replace("-", "/"))
    data["breach_start"] = data["breach_start"].str.replace("-", "/")
    for d, b in zip(data["Date_Posted_or_Updated"], data["breach_start"]):
        # handles days index in date list
        if b[1] in thirty_one:
            num_days = 31
        elif b[1] in thirty:
            num_days = 30
        elif b[0] in leap:
            num_days = 29
        else:
            num_days = 28
        start = datetime.strptime(b, '%Y/%m/%d')
        end = datetime.strptime(d, '%Y/%m/%d')
        delta = relativedelta.relativedelta(end, start)
        response_date.append(delta.months + (delta.years * 12) + (delta.days /
                                                                  num_days))
    data["response_date"] = pd.Series(response_date)
    return data


# research question 4
def clean_entities(data: pd.DataFrame) -> None:
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
