import dash
import dash_bootstrap_components as dbc
import flask
import models
from dash import dcc, html
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
from werkzeug.security import check_password_hash
from os import path
from app import _, server, app, login_manager, db, config, DWO
from apps import base, login

alerts=[]
###############################################################################
# Dash App's layout
app.title = config['SITE']['TITLE']

app.layout = dbc.Container([

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # Contents
    html.Div(id='page-content',
            className='my-1'
            ),

],fluid=False
)

###############################################################################
# Callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
)
def display_page(pathname):

    if pathname == '/logout':
        return login.layout()

    elif current_user.is_authenticated:
        global alerts
        a = alerts
        alerts=[]
        return base.layout(a)

    else:
        return login.layout()

@app.callback(Output('url', 'pathname'),
              Input('login-button', 'n_clicks'),
              State('email', 'value'),
              State('password', 'value'),
)
def authentication(n_clicks, email, password):

    login.alerts=[]

    if not n_clicks or current_user.is_authenticated:
        return '/'

    if not email:
        login.alerts.append(
            dbc.Alert(_('Email required!'),
                      color='danger',
                      dismissable=True,
                      className='my-1',
                     )
        )

    if not password:
        login.alerts.append(
            dbc.Alert(_('Password required!'),
                      color='danger',
                      dismissable=True,
                      className='my-1',
                     )
        )

    if len(login.alerts) > 0:
        return '/'

    else:
        # Authenticate user
        user = models.User.query.filter_by(email=email, active=True).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
            else:
                login.alerts.append(
                    dbc.Alert(_('Incorrect Password, try again!'),
                              color='danger',
                              dismissable=True,
                              className='my-1',
                             )
                )
        else:
            login.alerts.append(
                dbc.Alert(_('User not found!'),
                          color='danger',
                          dismissable=True,
                          className='my-1',
                         )
            )

        return '/'

###############################################################################
## Main
if __name__ == '__main__':

    if config['SITE']['DEBUG'] == 'True':
        DEBUG=True
    else:
        DEBUG=False

    # App DB Creation
    if not path.exists(config['APP']['DB_NAME']):
        db.create_all(app=server)
        print('Backend database created!')
    else:
        print('Backend database exists')

    # Test Data Warehouse DB connection
    try:
        if DWO.test_conn():
            print('Data Warehouse DB connection succeed!')
    except Exception as e:
        alerts.append(
            {'message':_('Data Warehouse unreachable!'), 'type':'danger'}
        )

    # Print Server version
    print(f"Dash v{dash.__version__}\n" \
          f"DCC v{dcc.__version__}\n" \
          f"DBC v{dbc.__version__}")

    # Run Server
    app.run_server(host='0.0.0.0', debug=DEBUG)

