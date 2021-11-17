"""home.py
"""
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from app import _

layout = dbc.Row([

    dbc.Col([

        dbc.Jumbotron([

            html.H3(_('Dashboard'), className='display-3'),

            html.Hr(className='my-2'),

            html.P(_('Data Visualization and Business Inteligence tool.'),
                   className='lead',
                  ),

        ]),

    ], className='p-0', width=12,
    ),
])
