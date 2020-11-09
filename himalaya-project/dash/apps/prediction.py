import datetime as dt
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash_table
import pandas as pd

from dash.dependencies import Input, Output, State
import os
import sys

root_dir = os.path.abspath('')
path_list = root_dir.split(os.sep)
himalaya_path =path_list[:-1]
himalaya_path = "\\".join(himalaya_path)

sys.path.insert(0, himalaya_path)
from peaks import Peaks


# Get peaks data
os.chdir(himalaya_path)
peak = Peaks().get_data()
peak = Peaks().clean_data(peak)
options_peaks = []

for i , row in peak.iterrows():
    options_peaks.append({'label':row['peak_name'], 'value': row['peak_id']})

os.chdir(root_dir)
app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = False

layout = html.Div(
    [dbc.Row([
            dbc.Col(html.Img(src="assets/logo_wagon.png", className="app__logo")),
            dbc.Col(html.H4("My PREDICTION SUBMISSION", className="header__text"), align='right')
            ]),

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
                                                html.Button(
                                                    "SUBMIT ENTRY",
                                                    id="submit-entry",
                                                    className="submit__button",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="container__1",
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="VIEW DATA ENTRY",
                            value="view-entry",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="entry-graph",
                                            figure={
                                                "data": [],
                                                "layout": {
                                                    "title": "Timestamp vs. Amount Pipetted (mL)",
                                                    "xaxis": {
                                                        "title": "Timestamp (YYYY-MM-DD HH-MM-SS)"
                                                    },
                                                    "yaxis": {
                                                        "title": "Amount Pipetted (mL)"
                                                    },
                                                    "annotations": [],
                                                    "margin": {"l": 50},
                                                },
                                            },
                                            config={"editable": True},
                                            className="graph__1",
                                        ),
                                        html.Br(),
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
                                    ],
                                    className="graph_container",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="entry-table",
                                                    style_cell={
                                                        "minWidth": "0px",
                                                        "maxWidth": "180px",
                                                        "whiteSpace": "normal",
                                                    },
                                                )
                                            ],
                                            className="table__1",
                                        )
                                    ],
                                    className="table__container",
                                ),
                            ],
                        ),
                    ],
                )
            ],
            className="tabs__container",
        ),
    ],
    className="app__container",
)


@app.callback(
    Output("tabs", "value"),
    [Input("submit-entry", "n_clicks")],
    [
        State("enter-operator-id", "value"),
        State("select-reagent", "value"),
        State("enter-time", "value"),
        State("enter-pipetted", "value"),
    ],
)
def entry_to_db(submit_entry, operator_id, reagent, time_elapsed, amount_pipetd):
    if submit_entry:
        sample_entry = [
            {
                "operator_id": operator_id,
                "reagent": reagent,
                "time_elapsed": time_elapsed,
                "amount_pipetted": amount_pipetd,
                "time_stamp": dt.datetime.now(),
            }
        ]
        insert_entry = connection.execute(db.insert(SQL_table), sample_entry)
        return "view-entry"
    raise dash.exceptions.PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)
