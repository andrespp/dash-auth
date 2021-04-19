"""users.py
"""
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app, DWO
from models import User

###############################################################################
# Report Definition

def layout():
    """Define dashboard layout
    """
    # New user Form
    signup_form = [

        dbc.FormGroup([
            dbc.Label('Name', html_for='name'),
            dbc.Input(type='text', id='name',
                      placeholder='First and Last Name'),
        ]),

        dbc.FormGroup([
            dbc.Label('Email', html_for='signup-email'),
            dbc.Input(type='email', id='email', placeholder='Enter email'),
        ]),

        dbc.FormGroup([
            dbc.Label('Password', html_for='password'),
            dbc.Input(type='password',
                      id='password',
                      placeholder='Enter password'
                     ),
        ]),

        dbc.FormGroup([
            dbc.Label('Password (Confirm)', html_for='password2'),
            dbc.Input(type='password',
                      id='password2',
                      placeholder='Confirm password'
                     ),
        ]),

    ]
    # modal
    modal = html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader('Add user'),
                    dbc.ModalBody(signup_form),
                    dbc.ModalFooter([
                        dbc.Button('Close', id='close', className='ml-auto'),
                        dbc.Button('Create new user',
                                   id='signup-button',
                                   color='primary',
                                   className='ml-1'
                                  ),

                    ]),
                ],
                id='modal',
            ),
        ]
    )

    # Page Layout
    layout = [

        # Title Row
        dbc.Row([

            dbc.Col(html.H5('System Users',
                           className='py-3 m-0 text-left'
                          ),
                    width={'size':4, 'offset':0},
                    className='px-3',
            ),

            dbc.Col(dbc.Button('Add User',
                               id='open',
                               color='secondary',
                               size='sm',
                               className='m-0 float-right',
                              ),
                    width={'size':4, 'offset':0},
                    className='py-3',
                   ),
        ],
            justify='between',
        ),

        # Graph Row
        dbc.Row([
            dbc.Col(
                html.Div(id='table1'),
            ),
        ]),

        # Modal Row
        dbc.Row(modal),

    ]

    return layout

###############################################################################
# Callbacks
@app.callback(
    Output('table1', 'children'),
    Input('table1','active_cell'),
)
def update_table1(active_cell):
    """update_table
    """

    df = lookup_data()

    table = dash_table.DataTable(
        columns=[{'name': i, 'id': i,
                  'type':'numeric',
                 } for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'textAlign':'center',
                    'minWidth':'100%',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                   },
        style_cell_conditional=[
            {'if': {'column_id': 'uid'},
             'width': '5%',
            },
            {'if': {'column_id': 'name'},
             'width': '20%',
            },
            {'if': {'column_id': 'active'},
             'width': '10%',
            },
        ],

        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None,
    ),
    return table

@app.callback(
    Output('modal', 'is_open'),
     Input('open', 'n_clicks'),
     Input('close', 'n_clicks'),
     State('modal', 'is_open'),
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

###############################################################################
# Data lookup functions

def lookup_data():
    """Lookup data
    """

    uid=[]
    user=[]
    email=[]
    created=[]
    modified=[]
    active=[]

    users = User.query.all()

    for i in users:
        uid.append(i.id)
        user.append(i.name)
        email.append(i.email)
        created.append(i.created)
        modified.append(i.modified)
        active.append(i.active)

    df = pd.DataFrame(
        {'uid':uid,
         'name':user,
         'email':email,
         'created':created,
         'modified':modified,
         'active':active,
        }
    )

    df['created'] = df['created'].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if x else None)
    df['modified'] = df['modified'].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if x else None)
    df['active'] = df['active'].apply(lambda x: 'X' if x else None)

    return df
