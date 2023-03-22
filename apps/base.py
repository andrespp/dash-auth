"""base.py
"""
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask_login import current_user, logout_user
from app import _, app, config, AUTH
from apps import home, users, sales, financial

###############################################################################
# Report Definition

def layout(alerts=None):
    """Define app layout

    Parameters
    ----------
        alerts | list of dicts
        Ex.:  [{'message':'This is an alert message', 'type':'danger'},
               {'message':'Another alert message', 'type':'success'}]

    """

    # Process alerts
    alert=[]
    if alerts:
        for i in alerts:
            alert.append(
                dbc.Alert(i['message'],
                          color=i['type'],
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
                    dbc.DropdownMenuItem(_('APPS'), header=True),
                    dbc.DropdownMenuItem(_('Sales'), href='/sales'),
                    dbc.DropdownMenuItem(_('Financial'), href='/financial'),
                ],
                nav=True,
                in_navbar=True,
                label=_('Dashboards'),
            ),

            # Dashboards Dropdown
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(_('Users'), href='/users'),
                    dbc.DropdownMenuItem(_('Groups'), href='/groups'),
                ],
                nav=True,
                in_navbar=True,
                label=_('Admin'),
            ),

            # Logout button
            dbc.NavLink(_('Logout'), href='/logout'),

        ],

        brand = _('Home'),
        brand_href='/',
        className='p-0',
    )

    ## Layout
    layout = dbc.Container([

        # Alerts
        dbc.Row(
            dbc.Col(alert,
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

    if AUTH and (not current_user.is_authenticated):
        return None

    else:
        if pathname =='/':
            return home.layout
        elif pathname[:7] =='/logout':
            logout_user()
            return None
        elif pathname =='/users':
            return users.layout()
        elif pathname =='/sales':
            return sales.layout()
        elif pathname =='/financial':
            return financial.layout()
        else:
            return html.Div([html.P(_('404 Page not found!'))])

