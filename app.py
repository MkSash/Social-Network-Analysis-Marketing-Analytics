import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as col
from operator import itemgetter
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output


edges = pd.read_csv('./data/edges.csv', usecols = ["User_1", "User_2"])
nodes = pd.read_csv('./data/nodes.csv', usecols = ["User_ID", "User", "Country"])
#dropping duplicate rows
edges.drop_duplicates(inplace=True)
nodes.drop_duplicates(inplace=True)

def plot_graph(country):
    
    if country == 'All':
        G = nx.from_pandas_edgelist(edges, "User_1", "User_2", create_using = nx.Graph())
    else:
        country_nodes = np.array(nodes[nodes['Country'] == country]['User_ID'])
        country_edges = edges.loc[edges['User_1'].isin(country_nodes)].loc[edges['User_2'].isin(country_nodes)]
        G = nx.from_pandas_edgelist(country_edges, "User_1", "User_2", create_using = nx.Graph())
    # position for each node
    pos = nx.spring_layout(G, seed=1111)
    
    # adding positions to graph
    for node, position in pos.items():
        G.nodes[node]['pos'] = position
        
    # edges for plot
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
        
    # nodes for plot
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hovertext=[],
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='RdBu',
            reversescale=True,
            color=[],
            size=15,
            colorbar=dict(
                thickness=10,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=0)))

    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        
    # coloring and adding informations to nodes
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        hovertext = str(adjacencies[0]) + ': ' + nodes[nodes['User_ID'] == adjacencies[0]]['User'].values[0]
        text = ' # of connections: ' + str(len(adjacencies[1]))
        node_trace['hovertext'] += tuple([hovertext])
        node_trace['text'] += tuple([text])
        
    # defining figure
    fig = {"data": [edge_trace, node_trace],
           "layout": go.Layout(
                font_color="#EAEAFF",
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[],
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))}

    
    # returning plot
    return fig



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = Dash(__name__, external_stylesheets = external_stylesheets)

colors = {
    'background': '#080844',
    'text': '#EAEAFF'
}

app.layout = layout = html.Div(style={'backgroundColor': colors['background'], 'padding': 20}, className="container", children=[
    html.Div(className="row", children = [
        html.H1('Social Network Visualizer', style={'fontSize': 50,
        'color': colors['text'],'fontFamily': "Serif"}),
        html.Div([
            html.P('Visualize your Linkedin Connections Network', style={'color': colors['text'], 'fontSize': 20, 'fontFamily': "Serif"}),
        ])
    ]), 
    html.Div(className="row", children=[ 
        html.Div(className='eight columns', children = [  
    dcc.Graph(id='graph-with-slider', style={'padding': 20})
        ]), 
        html.Div(className="four columns", children=[ 

        html.Div([
            html.P('Filter the Graph', style={'color': colors['text'], 'fontSize': 20, 'fontFamily': "Serif"}),
        ]),

        html.Div(style={'padding': 10, 'flex': 1}, children=[
        html.Label('Select the Country ', style={'color': colors['text'], 'fontFamily': "Serif"}),
     dcc.Dropdown(
        options=np.concatenate((np.array(['All']), nodes["Country"].unique()), axis=None),
        value='All',
        id='select_country'
    ),
        html.Br(),
        html.Label('Select the Profession ', style={'color': colors['text'], 'fontFamily': "Serif"}),
        dcc.Dropdown(['Job 1', 'Job 2', 'Job 3'], 'All'),

        html.Br(),
        html.Label('Highlight: ', style={'color': colors['text'], 'fontFamily': "Serif"}),
        dcc.RadioItems(['Influencers', 'Followers', 'Bridges','Neutrals', 'None'], 'None',  style={'color': colors['text']})
    ]), 


        ])

    ])

])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('select_country', 'value'))
def update_graph(country):
    return plot_graph(country)


if __name__ == '__main__':
    app.run_server(debug=True)


