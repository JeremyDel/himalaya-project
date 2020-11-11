import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash()

app.layout = html.Div(children=[
  # product header
  html.Div(children=[
    html.Img(src="http://demo.company.com/design/test_melissa/logo.png", alt="product")
  ], style={'padding' : 7, 'text-align' : 'center'}),
  html.Hr(style={'width' : '30%'}),
  # content
  html.Div(children=[
    html.H3("Please log in", hidden=False, id="page_header"),
    # login form
    html.Form(children=[
      html.P(children=["Username: ", dcc.Input(type='text', id='username', placeholder='username')]),
      html.P(children=["Password: ", dcc.Input(type='password', id='password', placeholder='password')]),
      html.Button(children=['Login'], type='submit', id='login_button')
      ], style={'width' : '30%', 'margin' : '0 auto'}, id="login_form", hidden=False)
    ], style={'display' : 'block', 'text-align' : 'center', 'padding' : 2}),
  html.Br(),
  html.Hr(style={'width' : '30%'}),
  # footer
  html.Div(children=[
    html.Img(src="http://demo.company.com/design/test_melissa/criteologo.png", alt="Logo")
    ], style={'padding' : 7, 'text-align' : 'center'})
  ])

@app.callback(Output('page_header', 'children'),
  events=[Event('login_button', 'click'), Event('login_form', 'click')],
  state=[State('username', 'value'), State('password', 'value')])
def login(username, password):
  if is_valid_user(username, password):
    return "You have been logged in"
  else:
    return "Wrong username/password please try again."

if __name__ == "__main__":
  app.run_server(debug=True)
