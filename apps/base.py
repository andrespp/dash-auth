"""base.py
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from flask_login import current_user, logout_user
from app import app, config, DWO
from apps import home, sales, financial

###############################################################################
# Report Definition

def layout():
    """Define app layout
    """

    alerts=[]

    # Test Data Warehouse DB connection
    try:
        if DWO.test_conn():
            print('Data Warehouse DB connection succeed!')
    except Exception as e:
        alerts.append(
            dbc.Alert('Data Warehouse unreachable!',
                      color='danger',
                      dismissable=True,
                      className='my-1',
                     )
        )

    ## Objects

    # Header
    header = html.H3(
        config['SITE']['HEADER'],
        style={'height':'62px',
               # https://cssgradient.io/
               'background':'rgb(2,0,36)',
               'background':'linear-gradient(180deg,' \
                                             'rgba(2,0,36,1) 0%,' \
                                             'rgba(77,77,80,1) 65%,' \
                                             'rgba(123,125,125,1) 100%)'
              },
        className='p-3 m-0 text-white text-center',
    )

    # Navbar
    navbar = dbc.NavbarSimple([

            # Dashboards Dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem('APPS', header=True),
                    dbc.DropdownMenuItem('Sales', href='/sales'),
                    dbc.DropdownMenuItem('Financial', href='/financial'),
                ],
                nav=True,
                in_navbar=True,
                label='Dashboards',
            ),

            # Logout button
            dbc.NavLink('Logout', href='/logout'),

        ],

        brand = 'Home',
        brand_href='/',
        className='p-0',
    )

    ## Layout
    layout = dbc.Container([

        # Alerts
        dbc.Row(
            dbc.Col(alerts,
                    width={'size':12, 'offset':0},
                    className='px-0',
            ),
        ),

        # Header Row
        dbc.Row(

            dbc.Col(header,
                    className='p-0',
                    width={'size':12, 'offset':0},
                   ),
                className='mt-3',

               ),

        # Navbar
        dbc.Row(dbc.Col(navbar,
                        className='p-0',
                        width={'size':12, 'offset':0},
                       ),
               ),

        # Contents
        html.Div(id='dashboard',
                className='my-1'
                ),

    ],fluid=False
    )

    return layout

###############################################################################
# Callbacks
@app.callback(Output('dashboard', 'children'),
              Input('url', 'pathname'),
)
def display_dashboard(pathname):

    if not current_user.is_authenticated:
        return None

    else:
        if pathname =='/':
            return home.layout
        elif pathname[:7] =='/logout':
            logout_user()
            return None
        elif pathname =='/sales':
            return sales.layout()
        elif pathname =='/financial':
            return financial.layout()
        else:
            return html.Div([html.P('404 Page not found!')])

