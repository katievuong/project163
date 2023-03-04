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
        result = []
        result = [int(d[i]) - int(b[i]) for i in range(len(d))]
        data["response_time"] = pd.Series(result)
    return data["response_time"]
