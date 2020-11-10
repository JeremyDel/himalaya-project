import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State
from data import Data
from weather import Weather
import datetime as dt
import re
import dash_table
import os
import sys
from peaks import Peaks
from xgb_model import HimalXGB

# bootstrap theme
# https://bootswatch.com/lux/
external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv('data/matching_table.csv')
df['summit_date'] = pd.to_datetime(df['summit_date'])

mylist = df.peak_name.unique()
peak_list = pd.DataFrame({'peak' : mylist})
season_list = ['Spring', 'Summer', 'Autumn', 'Winter', 'All']

years = [{'label':i, 'value' : str(i)} for i in range(df.year.min(), df.year.max()+1)]
years.append({'label' : df.year.max()+1, 'value' : 'All'})

weather = Weather().get_data()
weather = Weather().clean_data(weather)

peak = Peaks().get_data()
peak = Peaks().clean_data(peak)
options_peaks = []

for i , row in peak.iterrows():
    options_peaks.append({'label':row['peak_name'], 'value': row['peak_id']})

# ------------------------------------------------------------------------------
# defining layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Div([html.P("Host Country:",className="input__heading"),
                dcc.Dropdown(
                        id="select-host",
                        options=[{'label': 'Nepal', 'value': 'Nepal'},
                        {'label': 'China', 'value': 'China'},
                        {'label': 'India', 'value': 'India'},
                        {'label': 'Other', 'value': 'Unknown'}],
                        # value="EVER",
                        placeholder="Select host country",
                        className="host__select",
                        style={'width': '80%'},
                    )
                ])),

            dbc.Col(html.Div([html.P("Mountain and Route:",className="input__heading"),
                dcc.Dropdown(
                    id="select-mountain",
                    options=options_peaks,
                    # value="EVER",
                    placeholder="Select mountain",
                    className="peak__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Season:",className="input__heading"),
                dcc.Dropdown(
                    id="select-season",
                    options=[{'label': 'Winter', 'value': 'Winter'},
                    {'label': 'Summer', 'value': 'Summer'},
                    {'label': 'Spring', 'value': 'Spring'},
                    {'label': 'Autumn', 'value': 'Autumn'}],
                    # value="EVER",
                    placeholder="Select season",
                    className="season__select",
                    style={'width': '80%'},
                )
            ])),
            dbc.Col(html.Div([html.P("Status:",className="input__heading"),
                dcc.Dropdown(
                    id="select-status",
                    options=[{'label': 'Climber', 'value': 'climber'},
                    {'label': 'Sherpa', 'value': 'h-a worker'},
                    {'label': 'Media', 'value': 'media'},
                    {'label': 'Base camp member', 'value': 'bc member'},
                    {'label': 'Leader', 'value': 'leader'},
                    {'label': 'Deputy', 'value': 'deputy'},
                    {'label': 'Other', 'value': 'other'}],
                    # value="EVER",
                    placeholder="Select role in the expedition.",
                    className="status__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Commercial Route:",className="input__heading"),
                dcc.Dropdown(
                    id="select-comroute",
                    options=[{'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': "False"}],
                    # value="EVER",
                    placeholder="Commercial route? ",
                    className="rope__select",
                    style={'width': '80%'},
                )
            ])),
            dbc.Col(html.Div([html.P("Standard Route:",className="input__heading"),
                dcc.Dropdown(
                    id="select-standard",
                    options=[{'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': "False"}],
                    # value="EVER",
                    placeholder="Standard route ?",
                    className="rope__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Hired People:",className="input__heading"),
                dcc.Dropdown(
                    id="select-hired",
                    options=[{'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': "False"}],
                    # value="EVER",
                    placeholder="Hired people ?",
                    className="hired__select",
                    style={'width': '80%'},
                )
            ])),
            dbc.Col(html.Div([html.P("Fixed Rope:",className="input__heading"),
                dcc.Dropdown(
                    id="select-rope",
                    options=[{'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': "False"}],
                    # value="EVER",
                    placeholder="Fixed ropes ?",
                    className="rope__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),
        html.Br(),
        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Number of climbers:",className="input__heading"),
                daq.Slider(
                    id='slider-total',
                    min=0,
                    max=70,
                    step=1,
                    value=20,
                    size=350,
                    handleLabel={"showCurrentValue": True,"label": "Members"}
                )
            ])),
            dbc.Col(html.Div([html.P("Number of sherpas:",className="input__heading"),
                daq.Slider(
                    id='slider-hired',
                    min=0,
                    max=70,
                    step=1,
                    value=7,
                    size=350,
                    handleLabel={"showCurrentValue": True,"label": "Sherpas"}
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Number of days:",className="input__heading"),
                dbc.Input(
                    id='input-days',
                    type='number',
                    placeholder="Number of days",
                    style={'width': '65%'}
                )
            ])),
            dbc.Col(html.Div([html.P("Number of camps:",className="input__heading"),
                dbc.Input(
                    id='input-camps',
                    type='number',
                    placeholder="Number of camps",
                    style={'width': '65%'}
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Age of the person:",className="input__heading"),
                dbc.Input(
                    id='input-age',
                    type='number',
                    placeholder="Age of the person",
                    min=16,
                    style={'width': '65%'}
                )
            ])),
            dbc.Col(html.Div([html.P("Sex of the person:",className="input__heading"),
                dcc.Dropdown(
                    id="select-sex",
                    options=[{'label': 'Male', 'value': 1},
                    {'label': 'Female', 'value': 0}],
                    # value="EVER",
                    placeholder="Sex of the person",
                    className="sex__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),
        html.Br(),

        html.Div([
            daq.StopButton(
                id="submit-entry",
                size=120,
                buttonText='Calcul Prediction',
                className="submit__button"
            ),
        ]),

        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),

        daq.Gauge(
            id='gauge_score',
            label="SCORE",
            color={"gradient":True,"ranges":{"red":[0,40],"yellow":[40,60],"green":[60,100]}},
            min=0,
            max=100,
            value=0
        )
    ])
])

# @app.callback ----------------------------------------------------------------
@app.callback(
    Output("gauge_score", "value"),
    [Input("submit-entry", "n_clicks")],
    [
        State("select-mountain", "value"),
        State("select-host", "value"),
        State("input-days", "value"),
        State("input-camps", "value"),
        State("select-rope", "value"),
        State("slider-total", "value"),
        State("slider-hired", "value"),
        State("select-hired", "value"),
        State("select-comroute", "value"),
        State("select-standard", "value"),
        State("select-season", "value"),
        State("select-sex", "value"),
        State("select-status", "value"),
        State("input-age", "value"),

    ],
)

def dataframe_predict(submit_entry, mountain, host, days, camps, rope, total_members, total_hired, hired, comroute, stanroute, season, sex, status, age):

    to_predict = pd.DataFrame(columns=['peak_id', 'host', 'summit_days', 'camps', 'rope', 'tot_members',
       'tot_hired', 'no_hired', 'comrte', 'stdrte', 'peak_height',
       'sherpa_ratio', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour',
       'moon_illumination', 'DewPointC', 'FeelsLikeC', 'HeatIndexC',
       'WindGustKmph', 'cloudcover', 'humidity', 'precipMM', 'pressure',
       'visibility', 'winddirDegree', 'windspeedKmph', 'stability', 'season',
       'sex_M', 'status', 'age', 'cumul_snow'])



    if submit_entry:
        peak_height = peak[peak['peak_id']==mountain]['height_m'].values[0]
        sherpa_ratio = total_members/total_hired

        to_predict = to_predict.append({'peak_id':mountain, 'host':host, 'summit_days':int(days), 'camps':int(camps), 'rope':bool(rope), 'tot_members':int(total_members),
       'tot_hired':int(total_hired), 'no_hired':bool(hired), 'comrte': bool(comroute), 'stdrte':bool(stanroute), 'peak_height':peak_height,
       'sherpa_ratio': sherpa_ratio , 'maxtempC':-2.277021, 'mintempC': -9.736381, 'totalSnow_cm': 1.754977, 'sunHour': 10.275210,
       'moon_illumination': 48.470733, 'DewPointC' :-8.459432 , 'FeelsLikeC':-9.604752 , 'HeatIndexC': -5.661692,
       'WindGustKmph':13.669081, 'cloudcover': 45.633150, 'humidity': 81.966314, 'precipMM': 2.532628, 'pressure' : 1013.688569,
       'visibility':7.486308, 'winddirDegree':211.464793, 'windspeedKmph': 10.086931, 'stability': 0.045808, 'season' :season,
       'sex_M': int(sex), 'status': status, 'age': int(age), 'cumul_snow':43}, ignore_index=True)


        prediction = HimalXGB().predict_model(to_predict)

        return round(prediction[0][1]*100)


__name__ == '__main__'
app.run_server(debug=True)
