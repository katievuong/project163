import cleanup
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
pd.options.plotting.backend = "plotly"


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


def breach_individual_correlation(data: pd.DataFrame) -> None:
    # split the categories that are combined with a comma
    data['Type_of_Breach'] = data['Type_of_Breach'].str.split(', ')

    # create a new data frame with one row for each type of breach
    df = pd.DataFrame(data['Type_of_Breach'].explode().value_counts())
    df.reset_index(inplace=True)
    df.columns = ['Type_of_Breach', 'Count']

    # remove leading/trailing whitespaces from the breach types
    df['Type_of_Breach'] = df['Type_of_Breach'].astype(str).str.strip()

    # create a bar chart
    fig = px.bar(df, x='Type_of_Breach', y='Count', color='Type_of_Breach',
                 title='Number of Individuals Affected by Type of Breach')
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Number of Individuals Affected')
    fig.show()


def plot_average_response(data: pd.DataFrame) -> None:
    average = data.groupby('year')['response_date'].mean()
    # fig = px.box(data, x='year', y='response_date', title=
    #           # 'Average Response Rate 2002-2014')
    fig = average.plot(template="simple_white", labels=dict(
                       index="Year", value="Response Rate (Months)"))
    fig.update_layout(
        title='Average Response Rate From Breach Start Date 2002-2014',
                )
    fig.show()
    # return average


def plot_most_common_entity(data: pd.DataFrame) -> None:
    # horizontal bar plot
    entity_dict = cleanup.clean_entities(data)
    x_y = {'Type': entity_dict.keys(),
           'Values': entity_dict.values()}
    fig = px.bar(x_y, x='Values', y='Type', orientation='h')
    fig.update_layout(
        title='Amount of Breached Information According to Location',
        barmode='stack', yaxis={'categoryorder':
                                'total ascending'})
    fig.show()


def main():
    df1 = pd.read_csv("breaches.csv")
    df2 = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    plot_breaches_per_year(df1, df2)
    breach_individual_correlation(df1)


if __name__ == '__main__':
    main()
