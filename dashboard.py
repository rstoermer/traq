import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from functions import *
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#Colors: https://coolors.co/177e89-084c61-db3a34-ffc857-323031

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Generate the Dash App
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Gesamtportfolio', 'value': 'gesamtportfolio'},
            {'label': 'Kaufwert vs. Aktueller Wert', 'value': 'kaufwertVsAktuell'},
            {'label': 'Gewinn vs. Verlust', 'value': 'gewinnVerlust'},
            {'label': 'Einzelperformance', 'value': 'einzelperformance'}
        ],
        value='gewinnVerlust'
    ),
    dcc.Graph(id='graph',  style={'height': '94vh'})
    ]
)

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(selected_graph):
    if selected_graph == 'gesamtportfolio':
        print(selected_graph)
        #Read in the entire depot
        depot = serve_df()

        depotNow = depot.pivot_table(index='date', columns='position', values='total_value')

        #Group table by days
        #depotNow = depotNow.groupby(depotNow.index.date).mean()

        traces = []

        #Iterate through depot with current values and add them to the trace
        for position, values in depotNow.iteritems():
            traces.append(go.Scatter(x=values.index, y=values.values, name=position, stackgroup='A'))

        return {
            'data': traces,
            'layout': go.Layout(
                legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'},
                margin=go.layout.Margin(
                    l=40,
                    r=10,
                    b=30,
                    t=10,
                    pad=4
                )
            )
        }

    if selected_graph == 'einzelperformance':
        print(selected_graph)
        #Read in the entire depot
        depot = serve_df()

        #Create two dataframes, one for a time series of current values (depotNow) and one for a time series of value when bought (depotBuy)
        depotNow = depot.pivot_table(index='date', columns='position', values='total_value')
        depotBuy = depot.pivot_table(index='date', columns='position', values='total_value_buy')

        depotDiff = ((depotNow / depotBuy) - 1)*100
        depotDiff = depotDiff.groupby(depotDiff.index.date).mean()

        traces = []

        #Iterate through depot with current values and add them to the trace
        for position, values in depotDiff.iteritems():
            traces.append(go.Scatter(x=values.index, y=values.values, name=position))
            
        figure = go.Figure(data=traces)

        return {
            'data': traces,
            'layout': go.Layout(
                legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'},
                margin=go.layout.Margin(
                    l=40,
                    r=10,
                    b=30,
                    t=10,
                    pad=4
                )
            )
        }

    if selected_graph == 'kaufwertVsAktuell':
        print(selected_graph)

        #Read in the entire depot
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

        return {
            'data': traces,
            'layout': go.Layout(
                legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'},
                margin=go.layout.Margin(
                    l=40,
                    r=10,
                    b=30,
                    t=10,
                    pad=4
                )
            )
        }

    if selected_graph == 'gewinnVerlust':
        print(selected_graph)

        #Read in the entire depot
        depot = serve_df()

        #Create two dataframes, one for a time series of current values (depotNow) and one for a time series of value when bought (depotBuy)
        depotNow = depot.pivot_table(index='date', columns='position', values='total_value')
        depotBuy = depot.pivot_table(index='date', columns='position', values='total_value_buy')

        #Group table by days
        #depotNow = depotNow.groupby(depotNow.index.date).mean()
        #depotBuy = depotBuy.groupby(depotBuy.index.date).mean()

        #Create one additional dataframe to track the overall value of the portfolio compared to the value when bought
        depotOverall = pd.DataFrame()
        depotOverall['now'] = depotNow.sum(axis=1)
        depotOverall['buy'] = depotBuy.sum(axis=1)

        #Group by date
        depotOverall = depotOverall.groupby(depotOverall.index.date).mean()

        #Add diff and %
        depotOverall['diff'] = depotOverall['now'] - depotOverall['buy']
        depotOverall['%'] = ((depotOverall['now'] / depotOverall['buy']) - 1) * 100

        traces = []

        #Add overall value to the chart
        traces.append(go.Bar(x=depotOverall.index, y=depotOverall['diff'].values, name='Differenz'))
        traces.append(go.Scatter(x=depotOverall.index, y=depotOverall['%'].values, name='%', yaxis='y2', line = dict(
        color = ('rgb(180, 130, 0)'),
        width = 4,
        dash = 'dot')
                )
             )

        return {
            'data': traces,
            'layout': go.Layout(
                legend={'x': 0, 'y': 0, 'bgcolor': 'rgba(255,255,255,.65)'},
                margin=go.layout.Margin(
                    l=40,
                    r=30,
                    b=30,
                    t=10,
                    pad=4
                ),
                yaxis2=dict(
                    rangemode='tozero',
                    title='%',
                    overlaying='y',
                    side='right'
                ),
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True, host='localhost', port=8050)
