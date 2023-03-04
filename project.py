import pandas as pd
import plotly.express as px


def prc_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type of breach"].unique()


def vin_unique_breaches(data: pd.DataFrame) -> list[str]:
    return data["Type_of_Breach"].unique()


def plot_trend_line(data: pd.DataFrame) -> None:
    # fig = px.line(data, x="", y="", title="")
    # fig.show()
    pass


def plot_breach_types(data: pd.DataFrame) -> None:
    # fig = px.pie(data, values="", names="", title="")
    # fig.show()
    pass
