import pandas as pd


def prc_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type of breach"].unique()


def vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type_of_Breach"].unique()
