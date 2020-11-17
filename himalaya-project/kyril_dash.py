import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_html_components as html
from dash import no_update
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
import shap
from pickle import load

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

url_fatmap = "https://fatmap.com/@27.9880482,86.9248308,11734.4882324,-23.9999999,0,8620.6107686,normal"

feat_name = ['summit_days','camps','tot_members','tot_hired','peak_height','sherpa_ratio',
'maxtempC','mintempC','totalSnow_cm','sunHour','moon_illumination',
'DewPointC','FeelsLikeC','HeatIndexC','WindGustKmph',
'cloudcover','humidity','precipMM','pressure',
'visibility','winddirDegree','windspeedKmph',
'stability','sex_M','age','cumul_snow','peak_id_AMOT',
'peak_id_AMPH','peak_id_ANID','peak_id_ANN1','peak_id_ANN3',
'peak_id_ANN4','peak_id_ANNS','peak_id_APIM','peak_id_ARDN',
'peak_id_ARNK','peak_id_BAMO','peak_id_BARU','peak_id_BEDG',
'peak_id_BHRI','peak_id_BHRS','peak_id_BIJO','peak_id_BURK',
'peak_id_CBAM','peak_id_CHAG','peak_id_CHAM','peak_id_CHAN',
'peak_id_CHAW','peak_id_CHEK','peak_id_CHND','peak_id_CHOB',
'peak_id_CHOL','peak_id_CHOP','peak_id_CHOY','peak_id_CHRW',
'peak_id_CHUB','peak_id_CHUG','peak_id_CHUR','peak_id_CHUW',
'peak_id_CHWT','peak_id_DANS','peak_id_DHA1','peak_id_DHEC',
'peak_id_DING','peak_id_DOLM','peak_id_DOMK','peak_id_DOMO',
'peak_id_DRAN','peak_id_DZA2','peak_id_DZAS','peak_id_EVER',
'peak_id_FUTI','peak_id_GAN1','peak_id_GANC','peak_id_GAND',
'peak_id_GANG','peak_id_GANW','peak_id_GAUG','peak_id_GAUR',
'peak_id_GDNG','peak_id_GHUS','peak_id_GHYN','peak_id_GIME',
'peak_id_GIMM','peak_id_GOJN','peak_id_GORH','peak_id_GORK',
'peak_id_GYAJ','peak_id_GYLZ','peak_id_HCHI','peak_id_HIMJ',
'peak_id_HIML','peak_id_HMLE','peak_id_HNKU','peak_id_HONG',
'peak_id_HONK','peak_id_HUNK','peak_id_JABR','peak_id_JAGD',
'peak_id_JANE','peak_id_JANK','peak_id_JANU','peak_id_JOBO',
'peak_id_JOMS','peak_id_KAG1','peak_id_KAGA','peak_id_KANB',
'peak_id_KANG','peak_id_KANS','peak_id_KARY','peak_id_KCHN',
'peak_id_KCHS','peak_id_KGRI','peak_id_KHAM','peak_id_KIMS',
'peak_id_KNAG','peak_id_KOJI','peak_id_KORL','peak_id_KTEG',
'peak_id_KYAS','peak_id_KYAZ','peak_id_KYR1','peak_id_LANG',
'peak_id_LANR','peak_id_LANY','peak_id_LARK','peak_id_LAS2',
'peak_id_LCHA','peak_id_LCHN','peak_id_LDAK','peak_id_LDNG',
'peak_id_LHAY','peak_id_LHOT','peak_id_LIK1','peak_id_LIK2',
'peak_id_LMOC','peak_id_LNJU','peak_id_LOBE','peak_id_LSHR',
'peak_id_LSIS','peak_id_LUGU','peak_id_LUNR','peak_id_LUNW',
'peak_id_MAK2','peak_id_MAKA','peak_id_MALA','peak_id_MANA',
'peak_id_MNSL','peak_id_MUKT','peak_id_MUST','peak_id_NAG1',
'peak_id_NAG2','peak_id_NAN2','peak_id_NANG','peak_id_NGO3',
'peak_id_NGOJ','peak_id_NGOR','peak_id_NILN','peak_id_NILS',
'peak_id_NORB','peak_id_NPHU','peak_id_NUMB','peak_id_NUPL',
'peak_id_NUPT','peak_id_NUPW','peak_id_OMIT','peak_id_PAN1',
'peak_id_PAN2','peak_id_PANB','peak_id_PAND','peak_id_PANG',
'peak_id_PANN','peak_id_PATR','peak_id_PAWR','peak_id_PERI',
'peak_id_PHNH','peak_id_PHUG','peak_id_PK04','peak_id_PK41',
'peak_id_PKAR','peak_id_POKR','peak_id_POTA','peak_id_PUMO',
'peak_id_PURB','peak_id_PURK','peak_id_PUTH','peak_id_RAKS',
'peak_id_RATC','peak_id_RAUN','peak_id_RIPI','peak_id_ROLK',
'peak_id_ROLM','peak_id_ROMA','peak_id_SAIE','peak_id_SAIP',
'peak_id_SALW','peak_id_SAMD','peak_id_SANK','peak_id_SHEY',
'peak_id_SITA','peak_id_SPH1','peak_id_SPH2','peak_id_SPH4',
'peak_id_SYKG','peak_id_TAKP','peak_id_TASH','peak_id_TAWA',
'peak_id_TAWO','peak_id_TENE','peak_id_TENG','peak_id_TENR',
'peak_id_THAM','peak_id_THRK','peak_id_THUL','peak_id_TILI',
'peak_id_TILK','peak_id_TKPO','peak_id_TKRE','peak_id_TKRG',
'peak_id_TLNG','peak_id_TOBS','peak_id_TRIA','peak_id_TSAR',
'peak_id_TUKU','peak_id_URKM','peak_id_URMA','peak_id_YAKA',
'peak_id_YALU','peak_id_YANK','peak_id_YANS','peak_id_YARA',
'peak_id_YAUP','host_India','host_Nepal','host_Unknown',
'season_Spring','season_Summer','season_Winter','status_climber',
'status_deputy','status_h-a worker','status_leader','status_media','status_other',
'rope','no_hired','comrte','stdrte']

# ------------------------------------------------------------------------------
# defining layout
app.layout = html.Div([
    dbc.Container([

        html.Br(),
        html.Br(),

        html.Div(html.Iframe(src= url_fatmap,
                        style={'border': 'none', 'width': '100%', 'height': 500})),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    html.H3(children='Are you gonna reach the summit ?',
                                     className="text-center text-light bg-dark"),
                    body=True, color="dark")
            ,className="mb-4")
        ]),

        html.Div([
        dbc.Row([
            dbc.Col(html.Div([html.P("Host Country:",className="input__heading"),
                dcc.Dropdown(
                        id="select-host",
                        options=[{'label': 'Nepal', 'value': 'Nepal'},
                        {'label': 'China', 'value': 'China'},
                        {'label': 'India', 'value': 'India'},
                        {'label': 'Other', 'value': 'Unknown'}],
                        value="China",
                        placeholder="Select host country",
                        className="host__select",
                        style={'width': '80%'},
                    )
                ]),width={"size": 6}),

            dbc.Col(html.Div([html.P("Mountain and Route:",className="input__heading"),
                dcc.Dropdown(
                    id="select-mountain",
                    options=options_peaks,
                    value="EVER",
                    placeholder="Select mountain",
                    className="peak__select",
                    style={'width': '80%'},
                )
            ]),width={"size": 6})
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
                    value="Summer",
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
                    value="climber",
                    placeholder="Select role in the expedition",
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
                    value="True",
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
                    value="True",
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
                    value="True",
                    placeholder="Hired people ?",
                    className="hired__select",
                    style={'width': '80%'},
                )
            ])),
            dbc.Col(html.Div([html.P("Fixed Ropes:",className="input__heading"),
                dcc.Dropdown(
                    id="select-rope",
                    options=[{'label': 'Yes', 'value': 'True'},
                    {'label': 'No', 'value': "False"}],
                    value="True",
                    placeholder="Fixed ropes ?",
                    className="rope__select",
                    style={'width': '80%'},
                )
            ]))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(html.Div([html.P("Number of climbers:",className="input__heading"),
                html.Br(),
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
                html.Br(),
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
                    value =14,
                    placeholder="Number of days",
                    style={'width': '65%'}
                )
            ])),
            dbc.Col(html.Div([html.P("Number of camps:",className="input__heading"),
                dbc.Input(
                    id='input-camps',
                    type='number',
                    value= 5,
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
                    value=20,
                    style={'width': '65%'}
                )
            ])),
            dbc.Col(html.Div([html.P("Sex of the person:",className="input__heading"),
                dcc.Dropdown(
                    id="select-sex",
                    options=[{'label': 'Male', 'value': 1},
                    {'label': 'Female', 'value': 0}],
                    value=1,
                    placeholder="Sex of the person",
                    className="sex__select",
                    style={'width': '80%'},
                )
            ]))
        ]),] , style={'margin-bottom': '10px',
              'margin-left':'150px'}),

        html.Br(),
        html.Br(),

        html.Div([
            daq.StopButton(
                id="submit-entry",
                size=120,
                buttonText='Calcul Prediction',
                className="submit__button"
            ),
        ], style={'transform': 'translate(45%, 0)'}),

        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row([
            html.H5(children="Score", className="text-center"),
        ], justify="center", align="center"),

        dbc.Row([
            daq.Gauge(
                id='gauge_score',
                color={"gradient":True,"ranges":{"red":[0,40],"yellow":[40,60],"green":[60,100]}},
                min=0,
                max=100,
                value=0,
                showCurrentValue=True
            )
        ], justify="center", align="center"),

        html.Br(),

        dbc.Row([
            html.H5(children="Feature Impact", className="text-center")
            ], justify="center", align="center"),

        dbc.Row([
            dcc.Graph(id='shap')
        ], justify="center", align="center")
    ])
])

# @app.callback ----------------------------------------------------------------
@app.callback(
    [Output("gauge_score", "value"),
        Output("shap", "figure")],
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
        pred = round(prediction[0][1]*100)

        model = HimalXGB().load_model()
        pipe = load(open("pipeline.pkl","rb"))

        X = pipe.transform(to_predict)

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        test = pd.DataFrame(shap_values.T, columns=['value'])
        test['feature'] = feat_name
        test['abs_value'] = test['value'].map(abs)
        test = test[(test['value']>0.05)|(test['value']<-0.05)]
        test.sort_values(['abs_value'], inplace=True)

        fig = go.Figure(data=go.Bar(x=test.value,
                                    marker_color=test.abs_value))

        fig.update_yaxes(
            ticktext= list(test.feature),
            tickvals=list(range(0,len(test.feature))))

        fig.add_shape(type="line",
            xref="x", yref="paper",
            x0=0, y0=0, x1=0,y1=1,
            line=dict(
            color="black",
            width=2))

        fig.update_layout(
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',
            template = "seaborn",
            margin=dict(t=20))

        return pred, fig
    else:
        return (no_update, no_update)


__name__ == '__main__'
app.run_server(debug=True)
