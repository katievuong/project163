import pandas as pd


def prc_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type of breach"].unique()


def vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type_of_Breach"].unique()


def split_dates(data: pd.DataFrame) -> None:
    result = []
    data["Date_Posted_or_Updated"] = (data["Date_Posted_or_Updated"].str.split(
                                      "-"))
    data["breach_start"] = data["breach_start"].str.split("-")
    for d, b in zip(data["Date_Posted_or_Updated"], data["breach_start"]):
        result = [0, 0, 0]
        thirty = ["04", "06", "09", "11"]
        thirty_one = ["01", "03", "05", "07", "08", "10", "12"]
        leap = ["2004", "2008", "2012", "2016"]
        print(d, b)
        # handles days index in date list
        if b[1] in thirty_one:
            result[2] = 31 - int(b[2])
        elif b[1] in thirty:
            result[2] = 31 - int(b[2])
        elif b[0] in leap:
            result[2] = 29 - int(b[2])
        else:
            result[2] = 28 - int(b[2])
        result[2] += int(d[2])

        # handles months index
        if result[2] >= 31:
            result[2] -= 31
        if int(b[1]) > int(d[1]):
            result[1] = 12 - (int(b[1]) - int(d[1]))
        elif int(d[1]) - int(b[1]) != 1:
            result[1] = int(d[1]) - int(b[1])

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
            result[0] = int(d[0]) - int(b[0]) - 1
        data["response_time"] = pd.Series(result)
    return result


def apply_split(data: pd.DataFrame) -> None:
    data["response_time"] = data["response_time"].apply(split_dates(data))
    # return data["response_time"]
    pass
