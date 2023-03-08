import cleanup
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_breaches_per_year(data1: pd.DataFrame, data2: pd.DataFrame) -> None:
    # filter data by year
    data1 = data1[data1['year'].between(2009, 2017)]
    data2 = data2[data2['Year of Breach'].between(2009, 2017)]

    # count number of breaches per year for each dataset
    year_counts1 = data1['year'].value_counts().sort_index()
    year_counts2 = data2['Year of Breach'].value_counts().sort_index()

    # create plot data
    trace1 = go.Scatter(
        x=year_counts1.index,
        y=year_counts1.values,
        mode='lines+markers',
        name='Breaches in Dataset 1',
        line=dict(color='#007bff'),
        marker=dict(color='#007bff')
    )

    trace2 = go.Scatter(
        x=year_counts2.index,
        y=year_counts2.values,
        mode='lines+markers',
        name='Breaches in Dataset 2',
        line=dict(color='#ff7f0e'),
        marker=dict(color='#ff7f0e')
    )

    # create layout
    layout = go.Layout(
        title='Recent Data Breach Trends Over Time',
        xaxis=dict(
            title='Year',
            tickvals=[2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
            range=[2009, 2017]
        ),
        yaxis=dict(title='Number of Breaches')
    )

    # create figure and plot
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    fig.show()


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


def main():
    df1 = pd.read_csv("breaches.csv")
    df2 = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    plot_breaches_per_year(df1, df2)


if __name__ == '__main__':
    main()
