"""users.py
"""
import ast
import re
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import datetime as dt
import traceback
from dash import dcc, html, dash_table
from sqlalchemy.exc import IntegrityError
from dash.dependencies import Input, Output, State, ALL
from werkzeug.security import generate_password_hash
from app import _, app, db, DWO
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

            dbc.Col(html.H5(_('System Users'),
                           className='py-3 m-0 text-left'
                          ),
                    width={'size':4, 'offset':0},
                    className='px-3',
            ),

            dbc.Col(dbc.Button([_('Add User'),
                                html.I(className="fa fa-user-plus ml-2")
                               ],
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
        dbc.Row(get_signup_modal()),
        dbc.Row(get_user_edit_modal()),
        dbc.Row(get_user_remove_modal()),

    ]

    return layout

def get_signup_modal():
    """User signup modal
    """
    # New user Form
    signup_form = [

        html.Div(id='signup-alert'),

        dbc.FormGroup([
            dbc.Checklist(id='user-options',
                          options=[{'label':_('Active'), 'value':'active'}],
                          value=['active'],
                         ),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Name'), html_for='name'),
            dbc.Input(type='text', id='name',
                      placeholder=_('First and Last Name')),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Email'), html_for='email'),
            dbc.Input(type='email', id='email', placeholder=_('Enter email')),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Password'), html_for='password1'),
            dbc.Input(type='password',
                      id='password1',
                      placeholder=_('Enter password'),
                     ),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Password (Confirm)'), html_for='password2'),
            dbc.Input(type='password',
                      id='password2',
                      placeholder=_('Confirm password'),
                     ),
        ]),

    ]
    # modal
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader([_('Add user'), ]),
                    dbc.ModalBody(signup_form),
                    dbc.ModalFooter([
                        dbc.Button(_('Close'), id='close', className='ml-auto'),
                        dbc.Button(_('Clear Fields'), id='clear',
                                   className='ml-1'),
                        dbc.Button(_('Create new user'),
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


def get_user_edit_modal():
    """User edit modal
    """
    # user edit modal
    user_edit_form = [

        html.Div(id='user-edit-alert'),

        dbc.FormGroup([
            dbc.Checklist(id='user-options-edit',
                          options=[{'label':_('Active'), 'value':'active'}],
                          value=[],
                         ),
        ]),

        dbc.FormGroup(
            [
            dbc.Label(_('UID'), html_for='uid-edit'),
            dbc.Col(html.Div(id='uid-edit'),
                width=10, className='align-middle',
            ),
            ],
            row=True,
            className='m-0',
        ),

        dbc.FormGroup([
            dbc.Label(_('Name'), html_for='name-edit'),
            dbc.Input(type='text', id='name-edit',
                      placeholder=_('First and Last Name')),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Email'), html_for='email-edit'),
            dbc.Input(type='email',
                      placeholder=_('Enter email'),
                      disabled=True,
                      id='email-edit',
                     ),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Password'), html_for='password1-edit'),
            dbc.Input(type='password',
                      id='password1-edit',
                      placeholder=_('Enter password'),
                     ),
        ]),

        dbc.FormGroup([
            dbc.Label(_('Password (Confirm)'), html_for='password2-edit'),
            dbc.Input(type='password',
                      id='password2-edit',
                      placeholder=_('Confirm password'),
                     ),
        ]),

    ]

    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader([_('Edit User')]),
                    dbc.ModalBody(user_edit_form),
                    dbc.ModalFooter([
                        dbc.Button(_('Close'),
                                   className='ml-auto',
                                   size='sm',
                                   id='close-edit',
                                  ),
                        dbc.Button(_('Save'),
                                   id='save-edit',
                                   color='primary',
                                   size='sm',
                                   className='ml-1',
                                  ),
                    ]),
                ],
                is_open=False,
                id='user-edit-modal',
            )
        ]
    )

def get_user_remove_modal():
    """User remove modal
    """

    return html.Div(
        [
            html.Div(id='uid-remove', style={'display': 'none'}),

            dbc.Modal(
                [
                    dbc.ModalHeader([_('Remove User'),]),
                    dbc.ModalBody([
                        html.Div(id='user-remove-alert'),
                        html.P(id='user-remove-message')
                    ]),
                    dbc.ModalFooter([
                        dbc.Button(_('No'),
                                   className='ml-auto',
                                   size='sm',
                                   id='close-remove',
                                  ),
                        dbc.Button(_('Yes!'),
                                   id='save-remove',
                                   color='danger',
                                   size='sm',
                                   className='ml-1',
                                  ),
                    ]),
                ],
                is_open=False,
                id='user-remove-modal',
            )
        ]
    )

###############################################################################
# Callbacks
@app.callback(
    Output('table1', 'children'),
    Input('modal','is_open'),
    Input('signup-alert', 'children'),
    Input('user-edit-alert', 'children'),
    Input('user-remove-alert','children'),
)
def update_table1(is_open, signup, user_edit, user_remove):
    """update_table
    """
    df = lookup_data()

    # Add icons
    df[_('Active')] = df[_('Active')].apply(lambda x:
        html.I(className="fa fa-check") if x else None
    )

    df[_('Edit')] = df[_('UID')].apply(lambda x:
        dbc.Button(
            html.I(className="fa fa-user-edit"),
            color='light', size='sm',
            className='bg-transparent',
            id={'type':'update-user', 'index':x},
        )
    )

    df[_('Remove')] = df[_('UID')].apply(lambda x:
        dbc.Button(
            html.I(className="fa fa-trash-alt"),
            color='light', size='sm',
            id={'type':'remove-user', 'index':x},
        )
    )

    # Return table
    return dbc.Table.from_dataframe(df,
                                     striped=True,
                                     bordered=True,
                                     hover=True,
                                     responsive=True,
                                     size='sm',
                                     style={'textAlign':'center'}
                                    )

@app.callback(
    Output('modal', 'is_open'),
    Input('open', 'n_clicks'),
    Input('close', 'n_clicks'),
    State('modal', 'is_open'),
)
def toggle_modal(n1, n2, is_open):
    """toggle_modal()
    """
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('user-edit-modal','is_open'),
    Input({'type':'update-user', 'index':ALL}, 'n_clicks'),
    Input('close-edit', 'n_clicks'),
    State('user-edit-modal', 'is_open'),
)
def toggle_user_edit_modal(edit_btn, close_btn, is_open):
    """toggle_user_edit_modal()
    """

    # Identify callback context
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id=='close-edit':
        return False

    elif all([i == None for i in edit_btn]): # list is all None
        return is_open
    else:
        return True

@app.callback(
    Output('user-remove-modal','is_open'),
    Input({'type':'remove-user', 'index':ALL}, 'n_clicks'),
    Input('close-remove', 'n_clicks'),
    State('user-remove-modal', 'is_open'),
)
def toggle_user_remove_modal(remove_btn, close_btn, is_open):
    """toggle_user_remove_modal()
    """

    # Identify callback context
    ctx = dash.callback_context
    if not ctx.triggered:
        return False
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id=='close-remove':
        return False

    elif all([i == None for i in remove_btn]): # list is all None
        return is_open
    else:
        return True

@app.callback(
    Output('user-edit-alert','children'),
    Output('user-options-edit','value'),
    Output('name-edit','value'),
    Output('email-edit','value'),
    Output('uid-edit','children'),
    Input({'type':'update-user', 'index':ALL}, 'n_clicks'),
    Input('save-edit','n_clicks'),
    Input('user-edit-modal','is_open'),
    State('name-edit','value'),
    State('email-edit','value'),
    State('password1-edit','value'),
    State('password2-edit','value'),
    State('user-options-edit','value'),
    State('uid-edit','children'),
)
def user_edit_btn(edit_btn, save_btn, is_open, name, email, p1, p2, options,
                  uid):
    """user_edit_btn
    """

    r = {'name':name, 'email':email, 'options':options,
         'alert':None, 'uid':uid
        }

    # Identify which input fired the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        return r['alert'], r['options'], r['name'], r['email'], r['uid']
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Wasn't called by any edit button nor save-edit button
        if all([i == None for i in edit_btn]) and button_id != 'save-edit':
            return r['alert'], r['options'], r['name'], r['email'], r['uid']

        # Save user edit
        if button_id=='save-edit':

            if 'active' in r['options']:
                active=True
            else:
                active=False

            user_updated, msg = update_user(uid, name, email, p1, p2, active)
            if user_updated:
                r['alert'] = dbc.Alert(msg, dismissable=True, color='success')
            else:
                r['alert'] = dbc.Alert(msg, dismissable=True, color='danger')

            return r['alert'], r['options'], r['name'], r['email'], r['uid']

        # Close modal
        elif button_id=='user-edit-modal':
            return r['alert'], r['options'], r['name'], r['email'], r['uid']

        # User edit button
        else:
            button_id = ast.literal_eval(button_id)
            uid = button_id['index']

            # Fill user edit modal fields
            df = lookup_data()
            user = df[df[_('UID')]==uid]

            if len(user) == 1:
                user = user.iloc[0].to_dict()
                if user[_('Active')]:
                    r['options'] = ['active']

                return r['alert'], r['options'], \
                       user[_('Name')], user[_('Email')], uid

            else:
                return r['alert'], r['options'], r['name'], \
                       r['email'], r['uid']

@app.callback(
    Output('uid-remove','children'),
    Output('user-remove-message','children'),
    Output('user-remove-alert','children'),
    Input({'type':'remove-user', 'index':ALL}, 'n_clicks'),
    Input('save-remove','n_clicks'),
    State('user-remove-modal','is_open'),
    State('uid-remove','children'),
    State('user-remove-message','value'),
)
def user_remove_btn(remove_btn, save_btn, is_open, uid, msg):
    """user_remove_btn
    """
    alert = None

    # Identify which input fired the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        return uid, msg, alert
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Wasn't called by any remove button nor save-remove button
        if all([i == None for i in remove_btn]) and button_id != 'save-remove':
            return uid, msg, alert

        # Save user remove
        if button_id=='save-remove':

            # Perform user removal
            user_removed, message = remove_user(uid)
            if user_removed:
                alert = dbc.Alert(message, dismissable=True, color='success')
            else:
                alert = dbc.Alert(message, dismissable=True, color='danger')

            return uid, msg, alert

        # Close modal
        elif button_id=='user-remove-modal':
            return uid, msg, alert

        # User trash button
        else:
            button_id = ast.literal_eval(button_id)
            uid = button_id['index']
            msg = _('User') + f' {uid} ' + _('will be deleted.') + ' ' + \
                    _('Are you sure?')
            return uid, msg, alert

@app.callback(
    Output('signup-alert','children'),
    Output('name','value'),
    Output('email','value'),
    Output('password1','value'),
    Output('password2','value'),
    Input('signup-button','n_clicks'),
    Input('clear','n_clicks'),
    Input('modal','is_open'),
    State('name','value'),
    State('email','value'),
    State('password1','value'),
    State('password2','value'),
    State('user-options','value'),
)
def create_user_btn(btn, clear_btn, is_open, name, email, p1, p2, options):
    """create_user()
    """
    user = {'name':None, 'email':None, 'password':None, 'active':False}

    if not btn:
        return None, None, None, None, None #hh, name, email, p1, p2

    ctx = dash.callback_context

    if ctx.triggered:
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if btn_id == 'modal' or btn_id == 'clear':
            return None, None, None, None, None

    # Check user options
    if 'active' in options:
        user['active'] = True

    # Check Name
    if not name:
        return dbc.Alert(_('Name is empty'),
                         dismissable=True, color='danger'), name, email, p1, p2
    elif len(name.strip()) < 3:
        return dbc.Alert(_('User name too short.'),
                         dismissable=True, color='danger'), name, email, p1, p2
    elif not name.replace(" ", "").isalpha():
        return dbc.Alert(_('User name contains invalid characters.'),
                         dismissable=True, color='danger'), name, email, p1, p2
    else:
        user['name'] = name.strip()

    # Check email
    pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not email:
        return dbc.Alert(_('Email is empty'),
                         dismissable=True, color='danger'), name, email, p1, p2

    elif re.match(pattern, email):
        user['email'] = email
    else:
        return dbc.Alert(_('Invalid email'),
                         dismissable=True, color='danger'), name, email, p1, p2

    # Check password
    valid_password, msg = password_validation(p1, p2)
    if valid_password:
        user['password'] = p1
    else:
        return dbc.Alert(msg, dismissable=True,
                         color='danger'), name, email, None, None

    # Create user account / adduser / useradd
    try:
        usr = User(email=user['email'],
                    name=user['name'],
                    password=generate_password_hash(user['password'],
                                                    method='sha256'
                                                   ),
                    created=dt.datetime.today(),
                    active=user['active'],
                   )

        db.create_all()
        db.session.add(usr)
        db.session.commit()
        return dbc.Alert(_('Acount created!'),
                         dismissable=True,
                         color='success'), None, None, None, None
    except IntegrityError:
        db.session.rollback()
        return dbc.Alert(
            f_('Error creating account! User already exists'),
            dismissable=True, color='danger'), name, email, None, None
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return dbc.Alert(_('Error creating account:') + f' {e}',
                         dismissable=True, color='danger'), name, email, p1, p2

@app.callback(
    Output('name', 'invalid'),
    Output('name', 'title'),
    Input('name','value'),
)
def validate_signup_name(name):
    """Validade signup form
    """
    if not name: # blank cell is not invalid
        return False, None
    else:
        return name_check(name)

@app.callback(
    Output('name-edit', 'invalid'),
    Output('name-edit', 'title'),
    Input('name-edit','value'),
)
def validate_edit_name(name):
    """Validade edit form
    """
    return name_check(name)

@app.callback(
    Output('email', 'invalid'),
    Output('email', 'title'),
    Input('email','value'),
)
def validate_signup_email(email):
    """Validade signup form
    """
    if not email: # blank cell is not invalid
        return False, None
    else:
        return email_check(email)

@app.callback(
    Output('password1', 'invalid'),
    Output('password2', 'invalid'),
    Output('password1', 'title'),
    Output('password2', 'title'),
    Input('password1','value'),
    Input('password2','value'),
    Input('modal','is_open'),
    Input('signup-button','n_clicks'),
    State('password1','invalid'),
    State('password2','invalid'),
)
def validate_signup_password(p1, p2, is_open, btn, sp1, sp2):
    """Validade signup form
    """
    return validate_password_form(p1, p2, is_open, btn, sp1, sp2)

@app.callback(
    Output('password1-edit', 'invalid'),
    Output('password2-edit', 'invalid'),
    Output('password1-edit', 'title'),
    Output('password2-edit', 'title'),
    Input('password1-edit','value'),
    Input('password2-edit','value'),
    Input('user-edit-modal','is_open'),
    Input('save-edit','n_clicks'),
    State('password1-edit','invalid'),
    State('password2-edit','invalid'),
)
def validate_edit_password(p1, p2, is_open, btn, sp1, sp2):
    """Validade signup form
    """
    return validate_password_form(p1, p2, is_open, btn, sp1, sp2)

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
        {_('UID'):uid,
         _('Name'):user,
         _('Email'):email,
         _('Created'):created,
         _('Modified'):modified,
         _('Active'):active,
        }
    )

    df[_('Created')] = df[_('Created')].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if x else None)
    df[_('Modified')] = df[_('Modified')].apply(
        lambda x: x.strftime('%Y-%m-%d, %H:%M %Z') if pd.notnull(x) else None)
    df[_('Active')] = df[_('Active')].apply(lambda x: 'X' if x else None)

    return df

###############################################################################
# Other functions
def update_user(uid, name=None, email=None, p1=None, p2=None, active=None):
    """Update user

    Parameters
    ----------
        uid | int
        name | string
        email | string
        p1 | string -> password
        p2 | string -> password confirmation
        active | bool

    Returns
    -------
        (status, message), where 'status' is True if the updtate operation
        succeed, False otherwise, and 'message' is a string containing a
        message associated with the operation result
    """

    # Check password
    if p1 or p2:
        valid_password, msg = password_validation(p1, p2)
        if not valid_password:
            return False, msg

    # Update user
    try:
        user = User.query.filter_by(id=uid).first()
        user.name = name
        user.active = active
        user.modified=dt.datetime.now()
        if p1:
            user.password = generate_password_hash(p1, method='sha256')
        db.session.commit()
        return True, _('User successfully updated!')

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return False, _('Error updating user: ') + f'{e}'

def remove_user(uid):
    """Remove user

    Parameters
    ----------
        uid | int

    Returns
    -------
        (status, message), where 'status' is True if the updtate operation
        succeed, False otherwise, and 'message' is a string containing a
        message associated with the operation result
    """

    # Update user
    try:
        user = User.query.filter_by(id=uid).first()
        db.session.delete(user)
        db.session.commit()
        return True, _('User successfully deleted!')

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return False, _('Error deleting user: ') + f'{e}'

def name_check(name):
    """
    Verify if name is valid
    Returns (status, message), where status is True if name is valid or False
    otherwise, and message is a string with a message associated with
    the check result
    """
    # Check Name
    if not name:
        return False, _('Name not defined')
    elif len(name)==0:
        return False, _('Name not defined')
    else:
        name = name.strip()
        if len(name) < 3:
            return True, _('Name too short.')
        elif not name.replace(" ", "").isalpha():
            return True, _('Invalid characters.')
        else:
            return False, None

def email_check(email):
    """
    Verify if email is valid
    Returns (status, message), where status is True if email is valid or False
    otherwise, and message is a string with a message associated with
    the check result
    """
    # Check email
    pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.match(pattern, email)):
        return False, None
    else:
        return True, _('Invalid email')

    # Check Name
    name = name.strip()
    if len(name) < 3:
        return True, _('Name too short.')
    elif not name.replace(" ", "").isalpha():
        return True, _('Invalid characters.')
    else:
        return False, None

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(
        r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password
    ) is None

    # overall result
    password_ok = not (length_error or
                       digit_error or
                       uppercase_error or
                       lowercase_error or
                       symbol_error
                      )

    return {
        'ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }

def password_validation(p1, p2):
    """Validade passwords providaded in forms

    Returns (a, b), where 'a' is True if validations was successful of False
    otherwise, and 'b' a message associated with the validation.
    """
    if not p1:
        return False, _('Password is empty')

    pwd_check = password_check(p1)
    if not pwd_check['ok']:
        if pwd_check['length_error']:
            msg = _('The password must be at least 8 characters long.')
        elif pwd_check['digit_error']:
            msg = _('The password must have numbers.')
        elif pwd_check['uppercase_error'] or pwd_check['lowercase_error']:
            msg = _('The password must haver uppercase and lowercase letters.')
        elif pwd_check['symbol_error']:
            msg = _('The password must have special symbols.')
        return False, msg

    elif not p1==p2:
        return False, _('Passwords don\'t match.')
    else:
        return True, _('Passwords match.')

def validate_password_form(p1, p2, is_open, btn, sp1, sp2):
    """Validade password form
    Returns
        Output('password1', 'invalid'),
        Output('password2', 'invalid'),
        Output('password1', 'title'),
        Output('password2', 'title'),
    """
    invalid = {'p1':sp1, 'p2':sp2}
    title = {'p1':None, 'p2':None}

    ctx = dash.callback_context
    if ctx.triggered:
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if btn_id == 'modal' or btn_id == 'clear':
            return False, False, None, None

    if p1:
        pwd_check = password_check(p1)
        if not pwd_check['ok']:
            invalid['p1'] = True
            if pwd_check['length_error']:
                title['p1']= _(
                    'The password must be at least 8 characters long.'
                )
            elif pwd_check['digit_error']:
                title['p1'] = _('The password must have numbers.')
            elif pwd_check['uppercase_error'] or pwd_check['lowercase_error']:
                title['p1'] = _(
                    'The password must haver uppercase and lowercase letters.'
                )
            elif pwd_check['symbol_error']:
                title['p1'] = _('The password must have special symbols.')
        else:
            invalid['p1'] = False

    if p2:
        if not p1:
            invalid['p2'] = True
            title['p2'] = _('Fill password field.')
        elif not p1==p2:
            invalid['p2'] = True
            title['p2'] = _('Passwords don\'t match.')
        else:
            invalid['p2'] = False

    return invalid['p1'], invalid['p2'], title['p1'], title['p2']
