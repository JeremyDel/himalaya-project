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
              'height': '450px',
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
              children = [html.H1("Welcome to the Himalay-app dashboard", className="text-center",
                style={'color': 'white',
                       'text-align': 'center',
                        'position': 'absolute',
                        'top': '50%',
                        'left': '50%',
                        'transform': 'translate(-50%, -50%)',})]),

    html.Div(style={
              'background-color': '#ffffff',
              'background-repeat': 'no-repeat',
              'height': '450px',
              'background-position':'center',
              'position': 'relative',
              'background-size': 'cover',
              'width': '100vw',
              'margin-left' : '0',
              'margin-right' : '0',
              'margin-bottom': '0',
              'padding-left' : '0',
              'padding-right' : '0'
              },
              children = [

              html.H2("About the project", className="text-center", style={'color': 'black',
                                                                            'top': '40%',
                                                                            'transform': 'translate(0px, 40px)'}),
              html.Br(),
              html.Br(),
              html.Br(),

              dbc.Container([
                dbc.Row([dbc.Col(html.Div(children=[html.Img(src='assets/Hawley.jpg', height='100px')], style= {'border-radius': '100px'}), width=3),

                        dbc.Col(html.Div(children=[html.P("The dataset comes from Elizabeth Hawley. She was an American journalist, author, \
                          and chronicler of Himalayan mountaineering expeditions. Hawley's The Himalayan Database became the\
                          unofficial record for climbs in the Himalaya")]), align='center',
                          width=9)




                ]),

                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),

                dbc.Row([
                  dbc.Col(html.Div(children=[html.Img(src='assets/wagon.png', height='100px')], style= {'border-radius': '100px'}), width=3),

                        dbc.Col(html.P("We started this project as we were doing our bootcamp at Le Wagon Brussels.\
                          during this bootcamp we learned how to use data science tools, this project aims at showing of our skills\
                           learned during this bootcamp"),
                          align='center', width=9)



                ]),



              ])

          ]),

     html.Div(style={
              'background-color': '#2C2F33',
              'background-repeat': 'no-repeat',
              'height': '700px',
              'background-position':'center',
              'position': 'relative',
              'background-size': 'cover',
              'width': '100vw',
              'margin-left' : '0',
              'margin-right' : '0',
              'margin-bottom': '0',
              'padding-left' : '0',
              'padding-right' : '0'
              },
              children = [
              html.H2("About the team", className="text-center", style={'color': 'white',
                                                                        'top': '20%',
                                                                        'transform': 'translate(0px, 40px)'}),
              html.Br(),
              html.Br(),
              html.Br(),
              html.Br(),

              dbc.Container([dbc.CardDeck([

                dbc.Card([

                  dbc.CardImg(src="assets/kyril.jpg", top=True),
                  dbc.CardBody(children =[
                    html.H5(children='Kyril', className="text-center"),
                      html.Div(children="Kyril is our lead climber. Passionate about climbing and alpinism he came with the crazy idea\
                        of applying machine learning models to himalaya expeditions. His past experience as a data scientist\
                        helped the team further their skills.", className="card-text")]
                  ),
                ]),

                dbc.Card([

                  dbc.CardImg(src="assets/jerem.jpg", top=True),
                  dbc.CardBody(children =[
                    html.H5(children='Jeremy', className="text-center"),
                      html.Div(children="Jeremy is always there to pick up a challenge and find crazy ideas and bringing a solution to the table.\
                        He's not used to take the Standard Route to the top and he'll get you there by taking shortcuts.", className="card-text")]
                  ),
                ]),


                dbc.Card([

                  dbc.CardImg(src="assets/wafaa.jpg", top=True),
                  dbc.CardBody(children =[
                    html.H5(children='Wafaa', className="text-center"),
                      html.Div(children="Wafaa is the creative driving force of the project. Her visualizations skills helped us get\
                       through the data.", className="card-text")]
                  ),
                ]),

                dbc.Card([

                  dbc.CardImg(src="assets/nicolas.jpg", top=True),
                  dbc.CardBody(children =[
                    html.H5(children='Nicolas', className="text-center"),
                      html.Div(children="As Swiss, who has lived his whole life up in the mountains, this project suited him very well and didn't\
                       hesitated one second to pursue Kyril in this wonderful adventure. His knowlegde about alpinism greatly helped to team to further our analysis.", className="card-text")]
                  ),
                ]),




                ])

                ])

              ]),
    # dbc.Container([
    #     # dbc.Row([
    #     #     dbc.Col(html.Div(style={
    #     #       'background-image': "url('assets/background.jpg')",
    #     #       'background-repeat': 'no-repeat',
    #     #       'height': '400px',
    #     #       'background-position':'center',
    #     #       'position': 'relative',
    #     #       'background-size': 'cover',
    #     #       # 'width': '100%',
    #     #       # 'margin-left' : '0',
    #     #       # 'margin-right' : '0',
    #     #       # 'padding-left' : '0',
    #     #       # 'padding-right' : '0'
    #     #       },
    #     #       children = [html.H1("Welcome to the Himalay-app dashboard", className="text-center", style={'color': 'white'})]), className="mb-5", width =12)
    #     #     ]),

    #     dbc.Row([
    #         dbc.Col(html.H6(children='This app generates predictions and visualizations for himalaya expeditions'
    #                                  )
    #                 , className="mb-4")
    #         ]),

    #     dbc.Row([
    #         dbc.Col(html.H5(children='It consists of two main pages: Predictions, which aks for certain paramaters of a team member and the team itself and outputs a prediction, '
    #                                  'Visualizations, which gives an overview of the expeditions of the himalaya.')
    #                 , className="mb-5")
    #     ]),

    #     dbc.Row([
    #         dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
    #                                            className="text-center"),
    #                                    dbc.Row([dbc.Col(dbc.Button("Global", href="https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863",
    #                                                                color="primary"),
    #                                                     className="mt-3"),
    #                                             dbc.Col(dbc.Button("Singapore", href="https://data.world/hxchua/covid-19-singapore",
    #                                                                color="primary"),
    #                                                     className="mt-3")], justify="center")
    #                                    ],
    #                          body=True, color="dark", outline=True)
    #                 , width=4, className="mb-4"),

    #         dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
    #                                            className="text-center"),
    #                                    dbc.Button("GitHub",
    #                                               href="https://github.com/meredithwan/covid-dash-app",
    #                                               color="primary",
    #                                               className="mt-3"),
    #                                    ],
    #                          body=True, color="dark", outline=True)
    #                 , width=4, className="mb-4"),

    #         dbc.Col(dbc.Card(children=[html.H3(children='Read the Medium article detailing the process',
    #                                            className="text-center"),
    #                                    dbc.Button("Medium",
    #                                               href="https://medium.com/@meredithwan",
    #                                               color="primary",
    #                                               className="mt-3"),

    #                                    ],
    #                          body=True, color="dark", outline=True)
    #                 , width=4, className="mb-4")
    #     ], className="mb-5"),

    #     html.A("Special thanks to Flaticon for the icon in COVID-19 Dash's logo.",
    #            href="https://www.flaticon.com/free-icon/coronavirus_2913604")

    # ])

])

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)
