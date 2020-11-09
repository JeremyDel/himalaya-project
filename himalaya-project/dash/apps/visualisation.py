import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

# # bootstrap theme
# # https://bootswatch.com/lux/
# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------
# changing working directory to import data
import os
import sys


root_dir = os.path.abspath('')
path_list = root_dir.split(os.sep)
himalaya_path =path_list[:-1]
himalaya_path = "\\".join(himalaya_path)

sys.path.insert(0, himalaya_path)

from data import Data
from weather import Weather
# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = Data().get_matching_table()

mylist = df.peak_name.unique()
peak_list = pd.DataFrame({'peak' : mylist})
season_list = ['Spring', 'Summer', 'Autumn', 'Winter', 'All']

weather = Weather().get_data()
weather = Weather().clean_data(weather)

# ------------------------------------------------------------------------------
# return to current working directory
os.chdir(root_dir)

# ------------------------------------------------------------------------------
# App layout

layout = html.Div([
    dbc.Container([

        dcc.Dropdown(
            id='input_peak',
            options=[{'label':i, 'value':i} for i in peak_list['peak']],
            value='Everest'
        ),

        dcc.Slider(
            id='input_year',
            min=df.year.min(),
            max=df.year.max(),
            step=None,
            marks={i : str(i) for i in range(df.year.min(), df.year.max()+1)},
            value=df.year.max()
        ),

        dcc.RadioItems(
            id='input_season',
            options= [{'label':i, 'value':i} for i in season_list],
            value='All',
            labelStyle={'display': 'inline-block'}
        ),

# Peak Section # ---------------------------------------------------------------
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Peak',
                                     className="text-center text-light bg-dark"),
            body=True, color="dark")
            , className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(html.H5(children="Attempts", className="text-center"),
                width=6, className="mt-4"),
            dbc.Col(html.H5(children="Deaths by Altitude", className="text-center"),
                width=6, className="mt-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='peak_attempts'), width=6),
            dbc.Col(
                dcc.Graph(id='peak_death'), width=6)
        ]),

# Expedition & Member Section # ------------------------------------------------
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Expedition & Member',
                                     className="text-center text-light bg-dark"),
            body=True, color="dark")
            , className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(html.H5(children="Origin of Climbers", className="text-center"),
                width=6, className="mt-4"),
            dbc.Col(html.H5(children="Overall Success", className="text-center"),
                width=6, className="mt-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='exp_countries'), width=6),
            dbc.Col(
                dcc.Graph(id='exp_success'), width=6)
        ]),

        dbc.Row([
            dbc.Col(html.H5(children="Death's Reason", className="text-center"),
                width=6, className="mt-4"),
            dbc.Col(html.H5(children="Termination' Reason", className="text-center"),
                width=6, className="mt-4"),
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='exp_death'), width=6),
            dbc.Col(
                dcc.Graph(id='exp_term'), width=6)
        ]),

# Weather Section # ------------------------------------------------------------
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Historical Weather at Lobuche',
                                     className="text-center text-light bg-dark"),
            body=True, color="dark")
            , className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(html.H5(children="Temperature", className="text-center"),
                width=6, className="mt-4"),
            dbc.Col(html.H5(children="Rainfall", className="text-center"),
                width=6, className="mt-4"),
            dbc.Col(html.H5(children="Snowfall", className="text-center"),
                width=6, className="mt-4")
        ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='weather_temp'), width=6),
            dbc.Col(
                dcc.Graph(id='weather_rain'), width=6),
            dbc.Col(
                dcc.Graph(id='weather_snow'), width=6)
        ]),

    ])

])


# ------------------------------------------------------------------------------
# Peak callback # --------------------------------------------------------------

@app.callback(Output('peak_attempts', 'figure'),
                Output('peak_death', 'figure'),
                [Input('input_peak', 'value')],
                [Input('input_year', 'value')],
                [Input('input_season', 'value')])

def update_peak(peak, year, season):
    if season=='All':
        season = ''

    dff = df[(df.peak_name==peak)\
             &(df.year == int(year))\
             &(df.season.str.contains(season))]

    ts_fig = dff.groupby(['summit_date']).agg({'exp_id' : 'count'})
    ts_fig2 = dff[dff['death']==True].groupby(['death_height'], as_index= False)\
    .agg({'exp_id' : 'count'})
    ts_fig2.rename(columns={'exp_id' : 'Deaths',
                    'death_height' : 'Altitude'}, inplace=True)

    fig = go.Figure(
        data=[go.Scatter(x=ts_fig.index, y=ts_fig['exp_id'])]
        )

    fig.update_layout(
        yaxis={'title': "Daily Attempts"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    fig2 = go.Figure(data=[go.Scatter(x=ts_fig2["Altitude"],
                                      y=ts_fig2["Altitude"],
                                      mode='markers',
                                      text=ts_fig2['Deaths'],
                                      hoverinfo='text',
                                      marker=dict(size= ts_fig2['Deaths']*5))])

    fig2.update_xaxes(
        title_text = "Altitude (m)",
        showticklabels=True)

    fig2.update_yaxes(
        title_text = "",
        showticklabels=False)

    fig2.add_shape(type="line",
        xref="x", yref="paper",
        x0=8000, y0=0, x1=8000,y1=1,
        line=dict(
            color="black",
            width=2,
            dash = 'dot')
    )

    fig2.update_layout(
        yaxis={'title': "Number of Deaths"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    return fig, fig2

# Expeditions & Members callback # ---------------------------------------------
@app.callback(Output('exp_countries', 'figure'),
                Output('exp_success', 'figure'),
                Output('exp_death', 'figure'),
                Output('exp_term', 'figure'),
                [Input('input_peak', 'value')],
                [Input('input_year', 'value')],
                [Input('input_season', 'value')])

def update_exp(peak, year, season):
    if season=='All':
        season = ''

    dff = df[(df.peak_name==peak)\
             &(df.year == int(year))\
             &(df.season.str.contains(season))]

    term = dff.groupby(['citizenship'], as_index=False).agg({'exp_id':'count'})
    term.sort_values(by='exp_id', ascending=False, inplace=True)


    fig = go.Figure(data=[
        go.Bar(name='Countries', x=term['citizenship'], y=term['exp_id'])]
        )

    fig.update_layout(
        yaxis={'title': "Number of Climbers"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    dff_1 = dff[dff['summit_success']==1].groupby(['summit_date'])\
    .agg({'exp_id':'count'})
    dff_0 = dff[dff['summit_success']==0].groupby(['summit_date'])\
    .agg({'exp_id':'count'})

    fig1 = go.Figure(data=[
        go.Bar(name='Success', x=dff_1.index, y=dff_1['exp_id']),
        go.Bar(name='Failure', x=dff_0.index, y=dff_0['exp_id'])
    ])

    fig1.update_layout(
        barmode='stack',
        yaxis={'title': "Number of Successes and Failures"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

    death_val = dff.groupby(['death_type'], as_index=False).agg({'exp_id':'count'})
    labels = list(death_val.death_type.unique())
    labels.sort()
    parents = ['']*len(labels)
    values = list(death_val['exp_id'])

    fig2 = go.Figure(data = [go.Treemap(
        parents = parents,
        labels = labels,
        values = values,
        textinfo = "label+value",
        marker_colorscale = 'Blues')]
        )

    term = dff.groupby(['summit_term'], as_index=False).agg({'exp_id':'count'})
    term = term[term['summit_term'] != 'Success']
    term_labels = list(term.summit_term.unique())
    term_labels.sort()
    term_parents = ['']*len(term_labels)
    term_values = list(term['exp_id'])



    fig3 = go.Figure(data = [go.Treemap(
        parents = term_parents,
        labels = term_labels,
        values = term_values,
        textinfo = "label+value",
        marker_colorscale = 'Blues')]
        )

    return fig, fig1, fig2, fig3

# Weather callback # -----------------------------------------------------------
@app.callback(Output('weather_temp', 'figure'),
                Output('weather_rain', 'figure'),
                Output('weather_snow', 'figure'),
                [Input('input_peak', 'value')],
                [Input('input_year', 'value')],
                [Input('input_season', 'value')])

def update_exp(year, season):
    if season=='All':
        season = ''

    dff = df[(df.year == int(year))&(df.season.str.contains(season))]

    fig = go.Figure(
        data=[go.Scatter(x=ts_fig.index, y=ts_fig['exp_id'])]
        )

    fig.update_layout(
        yaxis={'title': "Daily Attempts"},
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)',
        template = "seaborn",
        margin=dict(t=20)
    )

# ------------------------------------------------------------------------------
__name__ == '__main__'
app.run_server(debug=True)
