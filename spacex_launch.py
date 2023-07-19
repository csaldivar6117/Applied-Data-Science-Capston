#Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                #TASK 1: Add a launch site drop-down input component
                                  dcc.Dropdown(id='site-dropdown',
                                                 options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                          ],
                                                    value='ALL',
                                                    placeholder="Select a Launch Site",
                                                    searchable=True
                                                ),
                                 html.Br(),

                                # Graph segment (TASK 2)
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                # Payload slider (TASK 3)
                                html.P("Payload range (Kg):"),
                                #TASK 3: Add a Range Slider to Select Payload
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,max=10000,step=1000,
                                                value=[min_payload,max_payload],
                                                marks={0: '0', 2500:'2500',5000:'5000',
                                                7500:'7500', 10000: '10000'}),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

#TASK 2: Add a callback function to render pie chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def build_graph(site_dropdown):
    filtered_df = spacex_df
    if site_dropdown == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Launches for All Sites')
        return fig
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        piechart = px.pie(filtered_df = specific_df, names='class',title='Total Launch for a Specific Site')
        return piechart

#TASK 4: Add a callback function to render the scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def update_graph(site_dropdown, payload_slider):
    filtered_df = spacex_df
    if site_dropdown == 'ALL':
        scatterplot = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return scatterplot
    else:
        specific_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        scatterplot = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
        return scatterplot

# Run the app
if __name__ == '__main__':
    app.run_server()    