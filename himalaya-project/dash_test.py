import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)

url = "https://fatmap.com/routeid/32880/everest-south-col-route?fmid=em"

app.layout = html.Div([
    html.Button('Submit',id='submit'),
    html.Embed(src=url, width="750",height="400"),
    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='submit', component_property='n_clicks')]
)

def update_output_div(n_clicks):
    if n_clicks:

        my_text = docx2txt.process("<path to .doc>")
        return 'You\'ve entered "{}"'.format(my_text)


__name__ == '__main__'
app.run_server(debug=True)
