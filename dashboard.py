import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from functions import *
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#generate charts
def serve_layout():
    depot = serve_df()

    #Create two dataframes, one for a time series of current values (depotNow) and one for a time series of value when bought (depotBuy)
    depotNow = depot.pivot_table(index='date', columns='position', values='total_value')

    traces = []

    #Iterate through depot with current values and add them to the trace
    for position, values in depotNow.iteritems():
        traces.append(go.Scatter(x=values.index, y=values.values, name=position, stackgroup='A'))

    return html.Div([dcc.Graph(id='Overview', style={'height': '100vh'}, figure={'data': traces,'layout': go.Layout(legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'})})])

def serve_layout2():
    depot = serve_df()
    
    #Create two dataframes, one for a time series of current values (depotNow) and one for a time series of value when bought (depotBuy)
    depotNow = depot.pivot_table(index='date', columns='position', values='total_value')
    depotBuy = depot.pivot_table(index='date', columns='position', values='total_value_buy')

    #Create one additional dataframe to track the overall value of the portfolio compared to the value when bought
    depotOverall = pd.DataFrame()
    depotOverall['now'] = depotNow.sum(axis=1)
    depotOverall['buy'] = depotBuy.sum(axis=1)

    traces = []

    #Add overall value to the chart
    traces.append(go.Scatter(x=depotOverall['now'].index, y=depotOverall['now'].values, name='Aktueller Gesamtwert', stackgroup='A'))
    traces.append(go.Scatter(x=depotOverall['buy'].index, y=depotOverall['buy'].values, name='Kaufwert', stackgroup='B'))

    return html.Div([dcc.Graph(id='Overview', style={'height': '100vh'}, figure={'data': traces,'layout': go.Layout(legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'})})])


#Generate the Dash App
app.layout = serve_layout()

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8050)
