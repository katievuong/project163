'''
Tyrell Garza, Kevin Fu, Katie Vuong

CSE 163

Data Breach Analysis: Investigating Trends and Impact on Businesses

Plotting file for outputting data visualizations drawing from both
breaches.csv and PRC Data Breach Chronology - 1.13.20.csv
'''
import cleanup
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# research question 1
def plot_breaches_per_year(data1: pd.DataFrame, data2: pd.DataFrame) -> None:
    '''

    Takes two dataframes, handles data in both to create two
    lines on one plot using plotly. Returns none.
    '''
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
    '''
    Takes in a dataframe and create a histagram that represent
    the average number of people who got affected by each type
    of the data breach. If there are multiply types for the same breach,
    it will consider the individuals to add on to all of the types of breah
    for that breach.
    '''
    df = data.copy()
    df['Type_of_Breach'] = df['Type_of_Breach'].str.split(', ')
    new_df = pd.DataFrame({'Type_of_Breach': df['Type_of_Breach'].explode(),
                           'Individuals_Affected':
                           df['Individuals_Affected'].repeat(df[
                              'Type_of_Breach'].str.len())})
    new_df['Type_of_Breach'] = new_df['Type_of_Breach'].astype(str).str.strip()
    new_df = (new_df.groupby('Type_of_Breach')
              ['Individuals_Affected'].mean().reset_index())
    fig = px.histogram(
        new_df, x='Type_of_Breach', y='Individuals_Affected',
        color='Type_of_Breach',
        title=(
               'Average Number of Individuals Affected by Type of Breach')
                       )
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Average Number of Individuals Affected',
                      xaxis_tickfont=dict(size=11))
    fig.show()


# research question 3
def plot_average_response(dataf: pd.DataFrame) -> None:
    '''
    Parameter: dataf - pandas dataframe
    Outputs a line graph that shows trend in data breach response rate based
    on the average time passed in months from 1997-2014 categorized by breach
    type, returns None
    '''
    df = cleanup.clean_breach_type(dataf)
    # Line graph
    average = df.groupby(
        ['year', 'Type_of_Breach'])['response_time'].mean().reset_index()

    fig = px.line(average, x='year', y='response_time',
                  color='Type_of_Breach', labels={'year': 'Year',
                                                  'response_time':
                                                  'Response Time (Months)'})
    fig.update_layout(
                title='Average Response Rate From Breach Start Date 1997-2014')
    fig.show()


# research question 4
def plot_most_common_entity(data: pd.DataFrame) -> None:
    '''
    Parameter: data - pandas dataframe
    Outputs a pie chart that displays different locations of breached
    information and the counts with a legend, returns None
    '''
    entity_dict = cleanup.clean_entities(data)
    # Pie chart
    x_y = {'Type': entity_dict.keys(),
           'Values': entity_dict.values()}
    fig = px.pie(x_y, values='Values', names='Type',
                 title='Amount of Breached Information According to Location',
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='label')
    fig.show()


# research question 5
def breach_individual_correlation(data: pd.DataFrame) -> None:
    '''

    Takes in breaches.csv dataframe and uses plotly to
    create a bar graph showing number of individuals
    affected by each type of breach. Uses plotly.
    Returns none.
    '''
    data = cleanup.clean_breach_type(data)

    # create a new data frame with one row for each type of breach
    df = pd.DataFrame(data['Type_of_Breach'].value_counts())
    df.reset_index(inplace=True)
    df.columns = ['Type_of_Breach', 'Count']

    # create a bar chart
    fig = px.bar(df, x='Type_of_Breach', y='Count', color='Type_of_Breach',
                 title='Total Number of Individuals Affected by Type of Breach'
                 )
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Number of Individuals Affected')
    fig.show()


def breach_total_records(data: pd.DataFrame) -> None:
    '''

    Takes in PRC dataframe and uses plotly to create a bar graph
    showing the total number of records for each type of breach.
    '''
    # remove commas from Total Records column
    data['Total Records'] = data['Total Records'].str.replace(',', '')

    # convert Total Records to integers
    data['Total Records'] = pd.to_numeric(data['Total Records'])

    # group by Type of breach and sum Total Records
    grouped_data = data.groupby(
        'Type of breach'
    )['Total Records'].sum().reset_index()

    # create bar chart
    fig = px.bar(grouped_data, x='Type of breach', y='Total Records',
                 title='PRC Clearinghouse Records Per Breach Type',
                 color='Type of breach')
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Total Records')
    fig.show()


# research question 6
def region_map_affected(data1: pd.DataFrame, data2: pd.DataFrame) -> None:
    '''
    Takes in two dataframe and plot a map of United States that shows the
    describution of the data breach by states based on the data.
    '''
    state_counts1 = data1['State'].value_counts().reset_index()
    state_counts1.columns = ['State', 'Count1']
    state_counts2 = data2['State'].value_counts().reset_index()
    state_counts2.columns = ['State', 'Count2']
    state_counts = state_counts1.merge(state_counts2, on='State', how='outer')
    state_counts['Total Count'] = (state_counts['Count1'].fillna(0) +
                                   state_counts['Count2'].fillna(0))
    state_counts.drop(columns=['Count1', 'Count2'], inplace=True)
    fig = go.Figure(data=go.Choropleth(
                    locations=state_counts['State'],
                    z=state_counts['Total Count'],
                    locationmode='USA-states',
                    colorscale='Reds',
                    zmin=0,
                    zmax=450,
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
    plot_average_response(cleanup.clean_dates(df1))
    plot_most_common_entity(df1)
    breach_individual_correlation(df1)
    breach_total_records(df2)
    region_map_affected(df1, df2)


if __name__ == '__main__':
    main()
