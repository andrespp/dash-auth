"""home.py
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

layout = dbc.Row([

    dbc.Col([

        dbc.Jumbotron([

            html.H3('Dashboard', className='display-3'),

            html.Hr(className='my-2'),

            html.P('Data Visualization and Business Inteligence tool.',
                   className='lead',
                  ),

        ]),

    ], className='p-0', width=12,
    ),
])
