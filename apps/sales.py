"""sales.py
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app, DWO

###############################################################################
# Report Definition

def layout():
    """Define dashboard layout
    """

    # Page Layout
    layout = [

            # Title Row
            dbc.Row([
                dbc.Col(html.P('Sales Dasboard',
                               className='p-5 m-0 text-center'
                              ),
                        width={'size':12, 'offset':0},
                        className='px-3',
                ),
            ]),

            # Graph Row
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='sales-graph01')
                ),
            ]),

    ]

    return layout

###############################################################################
# Callbacks

@app.callback(
    Output('sales-graph01','figure'),
    Input('sales-graph01','clickData'),
)
def update_graph01(click_data):
    """update_graph01 callback
    """

    # Lookup data
    df = lookup_data()

    # Transform data
    df = df.pivot(index='year',
                  columns='product',
                  values='sales',
    ).reset_index()

    # Build figure
    return px.bar(df, x='year', y=['A', 'B'], title="Produc Sales by year")


###############################################################################
# Data lookup functions
def lookup_data():
    """Lookup report data
    """

    sample_data = {
            'year':[2015, 2015, 2016, 2016, 2017, 2017, 2018, 2018],
            'product':'A B A B A B A B'.split(),
            'sales':[100, 200, 150, 250, 100, 350, 80, 250],
        }

    return pd.DataFrame(sample_data)

