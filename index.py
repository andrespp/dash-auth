import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
import models
from flask_login import login_user, login_required, logout_user, current_user
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output
from werkzeug.security import check_password_hash
from os import path
from app import server, app, db, config, DWO
from apps import home, login

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

        # Login button
        dbc.NavLink('Login', href='/login'),

        # Dashboards Dropdown
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Apps', header=True),
                dbc.DropdownMenuItem('Sales', href='#'),
                dbc.DropdownMenuItem('Finances', href='#'),
            ],
            nav=True,
            in_navbar=True,
            label='DASHBOARDS',
        ),

    ],

    brand = 'Home',
    brand_href='/',
    className='p-0',
)

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

# Dash App's layout
app.title = config['SITE']['TITLE']

app.layout = dbc.Container([

    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

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

    # Alerts
    dbc.Row(
        dbc.Col(alerts,
                width={'size':12, 'offset':0},
                className='p-0',
        ),
    ),

    # Contents
    html.Div(id='page-content',
            className='my-1'
            ),

],fluid=False
)

###############################################################################
# Flask Routes

@server.route('/')
def index():
    return flask.redirect(flask.url_for('/'))

@server.route('/login', methods=['GET', 'POST'])
def login_route():

    # Process form
    if flask.request.method == 'POST':

        # Retrieve login data
        email = flask.request.form.get('email')
        password = flask.request.form.get('password')

        # Authenticate user
        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flask.flash('Logged in successfully!', category='success')
                return flask.redirect(flask.url_for('/'))
            else:
                flask.flash('Incorrect password, try again.', category='error')
        else:
            flask.flash('User not found!', category='error')

    return flask.render_template('login.html', user='foo')

@server.route('/logout')
@login_required
def logout_route():
    logout_user()
    return flask.redirect('/login')

###############################################################################
# Callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
             )
@login_required
def display_page(pathname):
    err= html.Div([html.P('Page not found!')])
    switcher = {
        '/': home.layout,
        '/login': login.layout(),
    }
    return switcher.get(pathname, err)

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
    #server.run(host='0.0.0.0', debug=DEBUG)

