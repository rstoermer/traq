import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from functions import *
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def serve_layout():
    #Load the current depot
    con = db_connect()
    depot = pd.read_sql_query("SELECT * FROM accountholdings", con)
    con.close()

    #transform the dataframe
    depot['position'] = depot['account'] + " - " + depot['name']
    depot = depot.pivot_table(index='date', columns='position', values='total_value')

    traces = []
    for position, values in depot.iteritems():
        traces.append(go.Scatter(x=values.index, y=values.values, name=position, stackgroup='A'))

    return html.Div([dcc.Graph(id='Overview', style={'height': '100vh'}, figure={'data': traces,'layout': go.Layout(hovermode='closest')})])

#Generate the Dash App
app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.1.3', port=8050)
