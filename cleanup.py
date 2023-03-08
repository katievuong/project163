import pandas as pd


def prc_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type of breach"].unique()


def vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type_of_Breach"].unique()


# research question 3
def split_dates(data: pd.DataFrame) -> None:
    result = []
    response_date = []
    data["Date_Posted_or_Updated"] = (data["Date_Posted_or_Updated"].str.split(
                                      "-"))
    data["breach_start"] = data["breach_start"].str.split("-")
    num_days = 31
    for d, b in zip(data["Date_Posted_or_Updated"], data["breach_start"]):
        result = [0, 0, 0]
        thirty = ["04", "06", "09", "11"]
        thirty_one = ["01", "03", "05", "07", "08", "10", "12"]
        leap = ["2004", "2008", "2012", "2016"]
        # handles days index in date list
        if b[1] in thirty_one:
            result[2] = 31 - int(b[2])
        elif b[1] in thirty:
            result[2] = 31 - int(b[2])
        elif b[0] in leap:
            result[2] = (num_days - 2) - int(b[2])
        else:
            result[2] = (num_days - 3) - int(b[2])
        result[2] += int(d[2])

        # handles months index
        result[1] = result[2] / num_days
        if result[2] >= 31:
            result[2] -= 31
        if int(b[1]) > int(d[1]):
            result[1] += 12 - (int(b[1]) - int(d[1]))
        elif int(d[1]) - int(b[1]) != 1:
            result[1] += int(d[1]) - int(b[1])

        # handles years
        if int(d[0]) - int(b[0]) > 1:
            result[0] = int(d[0]) - int(b[0]) - 1
        elif int(d[0]) > int(b[0]) and int(d[1]) > int(b[1]):
            result[0] = int(d[0]) - int(b[0]) - 1
        elif int(d[0]) > int(b[0]) and (int(d[1]) == int(b[1]) and
                                        int(d[2]) >= int(b[2])):
            result[0] = int(d[0]) - int(b[0]) - 1
        elif int(d[0]) == int(b[0]) and (int(d[1]) == int(b[1]) and
                                         int(d[2]) >= int(b[2])):
            result[0] = int(d[0]) - int(b[0])
        result[1] += result[0] * 12
        response_date.append(result[1])
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
