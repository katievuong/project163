import cleanup
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
pd.options.plotting.backend = "plotly"


# research question 1
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


# research question 2
def average_number_affected(data: pd.DataFrame) -> None:
    df = data.copy()
    df['Individuals_Affected'] = df['Individuals_Affected'].astype(float)
    print(df)
    df = (
     df.groupby('Type_of_Breach')['Individuals_Affected'].mean().reset_index()
         )
    # Create a histogram plot
    fig = px.histogram(
        df, x='Type_of_Breach', y='Individuals_Affected',
        color='Type_of_Breach',
        title='Average Number of Individuals Affected by Type of Breach'
                      )
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Average Number of Individuals Affected')
    fig.show()


# research question 3
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


# research question 4
def plot_most_common_entity(data: pd.DataFrame) -> None:
    # pie chart
    entity_dict = cleanup.clean_entities(data)
    x_y = {'Type': entity_dict.keys(),
           'Values': entity_dict.values()}
    fig = px.pie(x_y, values='Values', names='Type',
                 title='Amount of Breached Information According to Location',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='label')
    fig.show()


# research question 5
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
                 title='Number of Individuals Affected by Type of Breach',
                 )
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Number of Individuals Affected')
    fig.show()


# research question 6
def region_map_affected(data1: pd.DataFrame, data2: pd.DataFrame) -> None:
    # Count breaches by state in dataset 1 and 2
    state_counts1 = data1['State'].value_counts().reset_index()
    state_counts1.columns = ['State', 'Count1']
    state_counts2 = data2['State'].value_counts().reset_index()
    state_counts2.columns = ['State', 'Count2']
    # Merge the two counts into a single dataframe
    state_counts = state_counts1.merge(state_counts2, on='State', how='outer')
    state_counts.fillna(0, inplace=True)
    # Create a choropleth map of the state-wise breach counts
    fig = go.Figure(data=go.Choropleth(
        locations=state_counts['State'],
        z=state_counts['Count1'] + state_counts['Count2'],
        locationmode='USA-states',
        colorscale='Reds',
        zmin=0,
        zmax=state_counts['Count1'].max() + state_counts['Count2'].max(),
        colorbar_title='Breach Counts'
    ))
    fig.update_layout(
        title_text='State-wise Breach Counts',
        geo_scope='usa',
    )
    fig.show()


def main():
    df1 = pd.read_csv("breaches.csv")
    df2 = pd.read_csv("PRC Data Breach Chronology - 1.13.20.csv")
    plot_breaches_per_year(df1, df2)
    average_number_affected(df1)
    plot_most_common_entity(df1)
    plot_average_response(cleanup.clean_dates(df1))
    breach_individual_correlation(df1)
    region_map_affected(df1, df2)


if __name__ == '__main__':
    main()
