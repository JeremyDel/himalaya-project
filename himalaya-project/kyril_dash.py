import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data import Data

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = Data().get_matching_table()

mylist = df.peak_id.unique()
peak_list = pd.DataFrame({'peak' : mylist})

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("HimalayApp", style={'text-align': 'center'}),

    dcc.RangeSlider(
        id='year_slider',
        min=2010,
        max=2020,
        step=1,
        value=[2010, 2020],
        marks= {i : str(i) for i in range(2010, 2021)}),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label':i, 'value':i} for i in peak_list['peak']]),

    html.Div(id='output', children=[]),
    html.Br()])


# # ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components
# @app.callback(
#     [Output(component_id='output_container', component_property='children'),
#      Output(component_id='output', component_property='children')],
#     [Input(component_id='year_slider', component_property='value')])



# # ------------------------------------------------------------------------------
__name__ == '__main__'
app.run_server(debug=True)
