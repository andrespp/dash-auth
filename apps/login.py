"""login.py
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


# Data lookup

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
            dbc.Input(type='password', id='password', placeholder='Enter password'),
        ]),

        dbc.Button('Login', color='secondary'),

    ]

    # Page Layout
    layout = [

        html.Form([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H3('Login Page'),
                ],
                    width=8,
                    className='text-center',
                ),
            ],
                justify='around',
                className='pt-3'
            ),

            # Form
            dbc.Row([

                dbc.Col(login_form,
                        className='p-0',
                        width=8,
                ),

            ],
                justify='around',
                className='py-3'
            ),

        ],
            method='POST',
        ),
    ]

    return layout

# Callbacks
