import cleanup
import plotly.express as px
import pandas as pd


def plot_trend_line(data: pd.DataFrame) -> None:
    # fig = px.line(data, x="", y="", title="")
    # fig.show()
    pass


def plot_average_response(data: pd.DataFrame) -> None:
    pass


def plot_most_common_entity(data: pd.DataFrame) -> None:
    # horizontal bar plot
    entity_dict = cleanup.clean_entities(data)
    print(entity_dict)
    x_y = {'type': entity_dict.keys(),
           'values': entity_dict.values()}
    fig = px.bar(x_y, x='values', y='type', orientation='h')
    fig.update_layout(barmode='stack',
                      yaxis={'categoryorder': 'total ascending'})
    fig.show()


def plot_breach_types(data: pd.DataFrame) -> None:
    # fig = px.pie(data, values="", names="", title="")
    # fig.show()
    pass
