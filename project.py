import pandas as pd


def unique_breaches(data: pd.DataFrame) -> int:
    return data["Type of breach"].unique()
