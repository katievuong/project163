import pandas as pd


def prc_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type of breach"].unique()


def vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type_of_Breach"].unique()


def split_dates(data: pd.DataFrame) -> None:
    data["Date_Posted_or_Updated"] = (data["Date_Posted_or_Updated"].str.split(
                                      "-"))
    data["breach_start"] = data["breach_start"].str.split("-")
    return data
