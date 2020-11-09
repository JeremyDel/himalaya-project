import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    html.Div(style={
              'background-image': "url('assets/background.jpg')",
              'background-repeat': 'no-repeat',
              'height': '400px',
              'background-position':'center',
              'position': 'relative',
              'background-size': 'cover',
              'width': '100vw',
              'margin-left' : '0',
              'margin-right' : '0',
              # 'margin-bottom': '80px',
              'padding-left' : '0',
              'padding-right' : '0'
              },
              children = [html.H1("Welcome to the Himalay-app dashboard", className="text-center", style={'color': 'white'})]),

    html.Div(style={
              'background-image': "url('assets/lines.png')",
              'background-repeat': 'no-repeat',
              'height': '700px',
              # 'background-position':'center',
              # 'position': 'relative',
              'background-size': 'cover',
              'width': '100%',
              'margin-left' : '0',
              'margin-right' : '0',
              'margin-bottom': '20px',
              'padding-left' : '0',
              'padding-right' : '0'
              },
              children = [html.H4("", className="text-center", style={'color': 'black'})]),
    dbc.Container([
        # dbc.Row([
        #     dbc.Col(html.Div(style={
        #       'background-image': "url('assets/background.jpg')",
        #       'background-repeat': 'no-repeat',
        #       'height': '400px',
        #       'background-position':'center',
        #       'position': 'relative',
        #       'background-size': 'cover',
        #       # 'width': '100%',
        #       # 'margin-left' : '0',
        #       # 'margin-right' : '0',
        #       # 'padding-left' : '0',
        #       # 'padding-right' : '0'
        #       },
        #       children = [html.H1("Welcome to the Himalay-app dashboard", className="text-center", style={'color': 'white'})]), className="mb-5", width =12)
        #     ]),

        dbc.Row([
            dbc.Col(html.H6(children='This app generates predictions and visualizations for himalaya expeditions'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='It consists of two main pages: Predictions, which aks for certain paramaters of a team member and the team itself and outputs a prediction, '
                                     'Visualizations, which gives an overview of the expeditions of the himalaya.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("Global", href="https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863",
                                                                   color="primary"),
                                                        className="mt-3"),
                                                dbc.Col(dbc.Button("Singapore", href="https://data.world/hxchua/covid-19-singapore",
                                                                   color="primary"),
                                                        className="mt-3")], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/meredithwan/covid-dash-app",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Read the Medium article detailing the process',
                                               className="text-center"),
                                       dbc.Button("Medium",
                                                  href="https://medium.com/@meredithwan",
                                                  color="primary",
                                                  className="mt-3"),

                                       ],
                             body=True, color="dark", outline=True)
                    , width=4, className="mb-4")
        ], className="mb-5"),

        html.A("Special thanks to Flaticon for the icon in COVID-19 Dash's logo.",
               href="https://www.flaticon.com/free-icon/coronavirus_2913604")

    ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)