import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def average_number_affected(data: pd.DataFrame) -> None:
   df = data.copy()
   df['Type_of_Breach'] = df['Type_of_Breach'].apply(lambda x: x.split(', '))
   df = df.explode('Type_of_Breach')
   df = df.groupby('Type_of_Breach')['Individuals_Affected'].mean().reset_index()
   df['Type_of_Breach'] = df['Type_of_Breach'].astype(str).str.strip()
   # Create a histogram plot
   new_df = pd.DataFrame({'Type of Breach': df['Type_of_Breach'].explode(),
                          'Individuals Affected': df['Individuals_Affected'].repeat(df['Type_of_Breach'].str.len())})
   fig = px.histogram(new_df, x='Type of Breach', y='Individuals Affected', color='Type of Breach',
                      title='Average Number of Individuals Affected by Type of Breach')
   fig.update_layout(xaxis_title='Type of Breach',
                     yaxis_title='Average Number of Individuals Affected',
                     xaxis_tickfont=dict(size=11))
   fig.update_traces(opacity=0.75)
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
    df3 = pd.read_csv("test.csv")
    average_number_affected(df1)


if __name__ == '__main__':
    main()