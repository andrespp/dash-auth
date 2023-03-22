"""home.py
"""
import dash_bootstrap_components as dbc
from dash import html
from app import _

jumbotron = html.Div(
    dbc.Container(
        [
            html.H3(_('Dashboard'), className='display-3'),
            html.Hr(className="my-2"),
            html.P(_('Data Visualization and Business Inteligence tool.'),
                   className='lead',
                  ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)

layout = dbc.Row(
    [
        dbc.Col([ jumbotron ], className='p-0', width=12, ),
    ]
)
