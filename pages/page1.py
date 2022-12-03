import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)


layout = html.Div(className="main", children=[
    html.Div(className="row", children = [
        html.H1('Social Network Analysis'),
        html.Div([
            html.P('Visualize your Linkedin Connections Network'),
        ])
    ]), 
    html.Div(className="row", children=[ 
        html.Div(className='eight columns', children = [  
            dcc.Graph(
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
        ]), 
        html.Div(className="four columns", children=[ 

        html.Div(style={'padding': 10, 'flex': 1}, children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['Country 1', 'Country 2', 'Country 3'], 'All'),
        html.Br(),
        html.Label('Dropdown'),
        dcc.Dropdown(['Job 1', 'Job 2', 'Job 3'], 'All'),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['Influencers', 'Bridges', 'All'], 'All')
    ]), 


        ])

    ])

])