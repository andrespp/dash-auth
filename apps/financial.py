"""financial.py
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import app

# Report Definition

def layout():
    """Define dashboard layout
    """

    # Page Layout
    layout = [

            dbc.Row([
                dbc.Col(html.P('Financial Dasboard',
                               className='p-5 m-0 text-center'
                              ),
                        width={'size':12, 'offset':0},
                        className='px-3',
                ),
            ]),

    ]

    return layout

