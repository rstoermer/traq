import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from functions import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Load the current depot
con = db_connect()
depot = pd.read_sql_query("SELECT * FROM accountholdings", con)
con.close()

#transform the dataframe
depot['position'] = depot['account'] + " - " + depot['name']
depot['date'] = depot['date'].apply(lambda x: x[:-10])



#Generate the Dash App
app.layout = html.Div(children=[
    html.H1(children='Visualisierung Depot'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)