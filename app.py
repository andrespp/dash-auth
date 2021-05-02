"""app.py
"""
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import configparser
import flask
import gettext
import locale
import models
import os.path
import uetl
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
_ = gettext.gettext

## Settings
CONFIG_FILE = 'config.ini'

# Read configuration File
if not os.path.isfile(CONFIG_FILE):
    print('ERROR: file "{}" does not exist'.format(CONFIG_FILE))
    exit(-1)
try:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
except:
    print('ERROR: Unable to read config file ("{}")'.format(CONFIG_FILE))
    exit(-1)

# Set locale
locale.setlocale(locale.LC_MONETARY, config['SITE']['LANG'])

if config['SITE']['LANG'].split('.')[0]=='pt_BR':
    pt_br = gettext.translation('messages',
                                localedir='locales',
                                languages=['pt-br'])
    pt_br.install()
    _ = pt_br.gettext # Brazilian portuguese

# Initialize Data Warehouse object
DWO = uetl.DataWarehouse(name=config['DW']['NAME'],
                         dbms=config['DW']['DBMS'],
                         host=config['DW']['HOST'],
                         port=config['DW']['PORT'],
                         base=config['DW']['BASE'],
                         user=config['DW']['USER'],
                         pswd=config['DW']['PASS'])

# Flask server
server = flask.Flask(__name__)
server.config['SECRET_KEY'] = config['APP']['SECRET_KEY']
server.config['SQLALCHEMY_DATABASE_URI'] = \
                                    f"sqlite:///{config['APP']['DB_NAME']}"
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Auth db
db = SQLAlchemy()
db.init_app(server)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(server)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

# Dash app object
THEME = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__,
                external_stylesheets=[THEME],
                server=server,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, \
                                        initial-scale=0.8,  \
                                        maximum-scale=1.0,  \
                                        minimum-scale=0.5,'
                            }]
               )
app.config.suppress_callback_exceptions=True

