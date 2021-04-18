"""login.py
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app

alerts=[]

# Report Definition

def layout():
    """Define page layout
    """
    # Login Form
    login_form = [

        dbc.FormGroup([
            dbc.Label('Email', html_for='email'),
            dbc.Input(type='email', id='email', placeholder='Enter email'),
        ]),

        dbc.FormGroup([
            dbc.Label('Password', html_for='password'),
            dbc.Input(type='password',
                      id='password',
                      placeholder='Enter password'
                     ),
        ]),

        dbc.Button('Login',
                   id='login-button',
                   type='submit',
                   color='secondary',
                  ),

    ]

    # Page Layout
    layout = [
        html.Div([

            # Alerts
            dbc.Row(
                dbc.Col(alerts,
                        width={'size':12, 'offset':0},
                        className='px-3',
                ),
            ),

            # Header
            dbc.Row([
                dbc.Col([
                    html.H3('Login Page'),
                ],
                    width=6,
                    className='text-center',
                ),
            ],
                justify='around',
                className='pt-5'
            ),

            # Form
            dbc.Row([

                dbc.Col(login_form,
                        className='p-0',
                        width=6,
                ),

            ],
                justify='around',
                className='py-3'
            ),

        ], className='p-5 mt-4')
    ]

    return layout

