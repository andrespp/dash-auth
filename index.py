import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import models
from flask_login import login_user, logout_user, current_user
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
from werkzeug.security import check_password_hash
from os import path
from app import server, app, db, config, DWO
from apps import home, login, sales, financial

###############################################################################
# Alerts

alerts=[]
if not DWO:
    alerts.append(
        dbc.Alert('Data Warehouse unreachable!',
                  color='danger',
                  dismissable=True,
                  className='my-1',
                 )
    )

###############################################################################
# Dash Components

# Header
header = html.H3(config['SITE']['HEADER'],
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

success = dbc.Container([

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

###############################################################################
# Dash App's layout
app.title = config['SITE']['TITLE']

app.layout = dbc.Container([

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # Alerts
    dbc.Row(
        dbc.Col(alerts,
                width={'size':12, 'offset':0},
                className='px-3',
        ),
    ),

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
        return success

    else:
        return login.layout()

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
            return sales.layout()
        else:
            return html.Div([html.P('404 Page not found!')])

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
            dbc.Alert('Email required!',
                      color='danger',
                      dismissable=True,
                      className='my-1',
                     )
        )

    if not password:
        login.alerts.append(
            dbc.Alert('Password required!',
                      color='danger',
                      dismissable=True,
                      className='my-1',
                     )
        )

    if len(login.alerts) > 0:
        return '/'

    else:
        # Authenticate user
        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
            else:
                login.alerts.append(
                    dbc.Alert('Incorrect Password, try again!',
                              color='danger',
                              dismissable=True,
                              className='my-1',
                             )
                )
        else:
            login.alerts.append(
                dbc.Alert('User not found!',
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

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = '/login'
    login_manager.init_app(server)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    # Print Server version
    print(f"Dash v{dash.__version__}.\n" \
          f"DCC v{dcc.__version__}.\n" \
          f"DBC v{dbc.__version__}")

    # Run Server
    app.run_server(host='0.0.0.0', debug=DEBUG)

