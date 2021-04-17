"""app.py
"""
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import configparser
import flask
import locale
import os.path
import traceback
import uetl

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

# Initialize Data Warehouse object
try:
    DWO = uetl.DataWarehouse(name=config['DW']['NAME'],
                             dbms=config['DW']['DBMS'],
                             host=config['DW']['HOST'],
                             port=config['DW']['PORT'],
                             base=config['DW']['BASE'],
                             user=config['DW']['USER'],
                             pswd=config['DW']['PASS'])
    # Test dw db connection
    if DWO.test_conn():
        print('Data Warehouse DB connection succeed!')
    else:
        print('ERROR: Data Warehouse DB connection failed!')
        exit(-1)
except Exception as e:
    DWO = None
    traceback.print_exc()

# Flask server
server = flask.Flask(__name__)
server.config['SECRET_KEY'] = config['SITE']['SECRET_KEY']

# Dash app object
THEME = dbc.themes.BOOTSTRAP
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[THEME],
                routes_pathname_prefix='/',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, \
                                        initial-scale=0.8,  \
                                        maximum-scale=1.0,  \
                                        minimum-scale=0.5,'
                            }]
               )
app.config.suppress_callback_exceptions=True

print(f"Dash v{dash.__version__}.\n" \
      f"DCC v{dcc.__version__}.\n" \
      f"DBC v{dbc.__version__}")

