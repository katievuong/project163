import cleanup
import plotly.express as px
import plotly.graph_objects as go
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
    x_y = {'Type': entity_dict.keys(),
           'Values': entity_dict.values()}
    fig = px.bar(x_y, x='Values', y='Type', orientation='h')
    fig.update_layout(barmode='stack',
                      yaxis={'categoryorder': 'total ascending'})
    fig.show()


def plot_breach_types(data: pd.DataFrame) -> None:
    # fig = px.pie(data, values="", names="", title="")
    # fig.show()
    pass


def plot_breaches_per_year(data):
    data = data[data['year'].between(2009, 2013)]  # filter by year
    year_counts = data['year'].value_counts().sort_index()

    # create plot data
    trace = go.Scatter(x=year_counts.index,
                       y=year_counts.values,
                       mode='lines+markers',
                       name='Number of Breaches',
                       line=dict(color='#007bff'),
                       marker=dict(color='#007bff'))

    # create layout
    layout = go.Layout(title='Recent Data Breach Trends Over Time',
                       xaxis=dict(title='Year',
                                  tickvals=[2009, 2010, 2011, 2012, 2013]),
                       yaxis=dict(title='Number of Breaches'))

    # create figure and plot
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()


def main():
    df = pd.read_csv("breaches.csv")
    plot_breaches_per_year(df)


if __name__ == '__main__':
    main()
