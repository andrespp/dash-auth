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
    # Page Layout
    layout = [

            # Title Row
            dbc.Row([
                dbc.Col(html.P('System Users',
                               className='p-5 m-0 text-center'
                              ),
                        width={'size':12, 'offset':0},
                        className='px-3',
                ),
            ]),

            # Graph Row
            dbc.Row([
                dbc.Col(
                    html.Div(id='table1'),
                ),
            ]),

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
        columns=[{"name": i, "id": i,
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
            {'if': {'column_id': 'id'},
             'width': '10%',
            },
            {'if': {'column_id': 'name'},
             'width': '20%',
            },
            #{'if': {'column_id': 'email'},
            # 'width': '50%',
            #},
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

    users = User.query.all()

    for i in users:
        uid.append(i.id)
        user.append(i.name)
        email.append(i.email)
        created.append(i.created)
        modified.append(i.modified)

    df = pd.DataFrame(
        {'uid':uid,
         'name':user,
         'email':email,
         'created':created,
         'modified':modified,
        }
    )

    df['created'] = df['created'].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if x else None)
    df['modified'] = df['modified'].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if x else None)

    return df
