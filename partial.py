import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def average_number_affected(data: pd.DataFrame) -> None:
    df = data.copy()
    df['Individuals_Affected'] = df['Individuals_Affected'].astype(float)
    df = df.groupby('Type_of_Breach')['Individuals_Affected'].mean().reset_index()
    # Create a histogram plot
    fig = px.histogram(df, x='Type_of_Breach', y='Individuals_Affected', color='Type_of_Breach',
                       title='Average Number of Individuals Affected by Type of Breach')
    fig.update_layout(xaxis_title='Type of Breach',
                      yaxis_title='Average Number of Individuals Affected')
    fig.show()




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
    average_number_affected(df1)
    region_map_affected(df1, df2)


if __name__ == '__main__':
    main()