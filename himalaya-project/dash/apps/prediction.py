# ------------------------------------------------------------------------------
# imports
import datetime as dt
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

import dash_table
import pandas as pd
from app import app

from dash.dependencies import Input, Output, State
import os
import sys

root_dir = os.path.abspath('')
path_list = root_dir.split(os.sep)
himalaya_path =path_list[:-1]
himalaya_path = "\\".join(himalaya_path)

sys.path.insert(0, himalaya_path)

from peaks import Peaks
from xgb_model import HimalXGB

# ------------------------------------------------------------------------------
# changing working directory to import data

os.chdir(himalaya_path)
peak = Peaks().get_data()
peak = Peaks().clean_data(peak)
options_peaks = []

for i , row in peak.iterrows():
    options_peaks.append({'label':row['peak_name'], 'value': row['peak_id']})

# ------------------------------------------------------------------------------
# return to current working directory
os.chdir(root_dir)

# # ------------------------------------------------------------------------------
# # run that for single page element
# app = dash.Dash(__name__)
# server = app.server

# app.config.suppress_callback_exceptions = False

# ------------------------------------------------------------------------------
# defining layot
layout = html.Div(
    [

        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="data-entry",
                    children=[
                        dcc.Tab(
                            label="DATA ENTRY",
                            value="data-entry",
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Host Country:",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-host",
                                                    options=[{'label': 'Nepal', 'value': 'Nepal'},
                                                    {'label': 'China', 'value': 'China'},
                                                    {'label': 'India', 'value': 'India'},
                                                    {'label': 'Other', 'value': 'Unknown'}],
                                                    # value="EVER",
                                                    placeholder="Select host country.",
                                                    className="host__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                            'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Moutain and Route:",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-mountain",
                                                    options=options_peaks,
                                                    # value="EVER",
                                                    placeholder="Select mountain.",
                                                    className="peak__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                            'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Season:",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-season",
                                                    options=[{'label': 'Winter', 'value': 'Winter'},
                                                    {'label': 'Summer', 'value': 'Summer'},
                                                    {'label': 'Spring', 'value': 'Spring'},
                                                    {'label': 'Autumn', 'value': 'Autumn'}],
                                                    # value="EVER",
                                                    placeholder="Select season of the expedition.",
                                                    className="season__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Status:",
                                                    className="input__heading",
                                                ),
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
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                            'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Total members of the Expedition",
                                                    className="input__heading",
                                                    style={'margin-bottom':'40px'}
                                                ),
                                                daq.Slider(
                                                    id='slider-total',
                                                    min=0,
                                                    max=70,
                                                    step=1,
                                                    value=20,
                                                    size=500,
                                                    handleLabel={"showCurrentValue": True,"label": "VALUE"}
                                                ),
                                            ],
                                            className="slider-output-container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Amount of days planned:",
                                                    className="input__heading",
                                                ),

                                                dbc.Input(
                                                    id='input-days',
                                                    type='number',
                                                    placeholder="Number of days",
                                                    value=20,
                                                    size='40px'

                                                ),
                                            ],
                                            className="input__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Amount of camps planned:",
                                                    className="input__heading",
                                                ),

                                                dbc.Input(
                                                    id='input-camps',
                                                    type='number',
                                                    placeholder="Number of camps",
                                                    value=8,
                                                    size='40px'

                                                ),
                                            ],
                                            className="input__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),

                                        html.Div(
                                            [
                                                html.P(
                                                    "Will you follow a commercial route",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-comroute",
                                                    options=[{'label': 'Yes', 'value': 'True'},
                                                    {'label': 'No', 'value': "False"}],
                                                    # value="EVER",
                                                    placeholder="commercial route? ",
                                                    className="rope__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Will you follow the standard route to the summit",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-standard",
                                                    options=[{'label': 'Yes', 'value': 'True'},
                                                    {'label': 'No', 'value': "False"}],
                                                    # value="EVER",
                                                    placeholder="Standard route ?",
                                                    className="rope__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "People hired y/n:",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-hired",
                                                    options=[{'label': 'Yes', 'value': 'True'},
                                                    {'label': 'No', 'value': "False"}],
                                                    # value="EVER",
                                                    placeholder="Were some people hired to help with expedition",
                                                    className="hired__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Fixed ropes y/n",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-rope",
                                                    options=[{'label': 'Yes', 'value': 'True'},
                                                    {'label': 'No', 'value': "False"}],
                                                    # value="EVER",
                                                    placeholder="planning to place fixed ropes",
                                                    className="rope__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Number of peple hired:",
                                                    className="input__heading",
                                                    style={'margin-bottom':'40px'}
                                                ),
                                                daq.Slider(
                                                    id='slider-hired',
                                                    min=0,
                                                    max=70,
                                                    step=1,
                                                    value=7,
                                                    size=500,
                                                    handleLabel={"showCurrentValue": True,"label": "VALUE"}
                                                ),
                                            ],
                                            className="slider-output-container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Age:",
                                                    className="input__heading",
                                                ),

                                                dbc.Input(
                                                    id='input-age',
                                                    type='number',
                                                    placeholder="Age of the person",
                                                    value=30,
                                                    min=16

                                                ),
                                            ],
                                            className="input__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Sex",
                                                    className="input__heading",
                                                ),
                                                dcc.Dropdown(
                                                    id="select-sex",
                                                    options=[{'label': 'Male', 'value': 1},
                                                    {'label': 'Female', 'value': 0}],
                                                    # value="EVER",
                                                    placeholder="Sex of the person",
                                                    className="sex__select",
                                                    style={'width': '50%'},
                                                ),
                                            ],
                                            className="dropdown__container",
                                            style={'margin-left': '40px',
                                                    'margin-bottom': '10px'},
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.Button(
                                                    "SUBMIT ENTRY",
                                                    id="submit-entry",
                                                    className="submit__button",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="container__1",
                                    # style={'background-image': "url('assets/mountain_colors.png')",
                                    #               'background-repeat': 'no-repeat',
                                    #               'height': '400px',
                                    #               'background-position':'right',
                                    #               'position': 'relative',
                                    #               'background-size': 'cover'},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="VIEW DATA ENTRY",
                            value="view-entry",
                            children=[
                                html.Div(
                                    [
                                        html.H5(id='fail-succes', style={'margin-bottom': '40px'}),

                                        html.Div(
                                            children=[
                                                html.Button(
                                                    "ADD ANNOTATION",
                                                    id="add-button",
                                                    style={"margin-right": "2.5%"},
                                                    className="add__button",
                                                ),
                                                html.Button(
                                                    "DELETE ANNOTATION",
                                                    id="delete-button",
                                                    style={"margin-right": "2.5%"},
                                                    className="del__button",
                                                ),
                                                html.Button(
                                                    "CLEAR DATA",
                                                    id="clear-button",
                                                    style={"margin-right": "2.5%"},
                                                    className="clear__button",
                                                ),
                                            ]
                                        ),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                    ],
                                    className="app_container",
                                ),
                            ],
                        ),

                    ],
                )
            ],
            className="tabs__container",
        ),

        html.Footer(dbc.Row([
                dbc.Col(html.Img(src="assets/logo_wagon.png", className="app__logo"), width=10),
                dbc.Col(html.H4("My PREDICTION SUBMISSION", className="header__text"), width=2, align='right')])),

    ],
    className="app__container",
)


# @app.callback
@app.callback(
    Output("fail-succes", "children"),
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

        os.chdir(himalaya_path)

        prediction = HimalXGB().predict_model(to_predict)

        os.chdir(root_dir)

        if prediction[0][2] == 1:
            return f"This person will succeed the expedition with a {round(100*prediction[0][1], 2)}% chance"
        if prediction[0][2] == 0:
            return f"Unfortunately this person will most likely fail the expedition with a {round(100*prediction[0][0], 2)}% chance"
        raise dash.exceptions.PreventUpdate


# # def entry_to_db(submit_entry, operator_id, reagent, time_elapsed, amount_pipetd):
#     if submit_entry:
#         sample_entry = [
#             {
#                 "operator_id": operator_id,
#                 "reagent": reagent,
#                 "time_elapsed": time_elapsed,
#                 "amount_pipetted": amount_pipetd,
#                 "time_stamp": dt.datetime.now(),
#             }
#         ]
#         insert_entry = connection.execute(db.insert(SQL_table), sample_entry)
#         return "view-entry"
#     raise dash.exceptions.PreventUpdate

# if __name__ == "__main__":
#     app.run_server(debug=True)
