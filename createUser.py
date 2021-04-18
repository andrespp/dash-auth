#!/usr/bin/env python3
"""create_user.py
"""
import re
import sys
import errno
import argparse
from models import User
from app import server, db
from getpass import getpass
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

parser = argparse.ArgumentParser(description='User add tool')
parser.add_argument('-n',
                    '--name',
                    type=str,
                    required=True,
                    help='User name',
                    metavar='"John Doe"')
parser.add_argument('-e',
                    '--email',
                    type=str,
                    required=True,
                    help='Email',
                    metavar='foo@bar.com')
parser.add_argument('-p',
                    '--password',
                    type=str,
                    help="Password",
                    metavar='secret')

if __name__ == '__main__':

    # Argparse
    args = parser.parse_args()

    # Check Name
    if args.name.replace(" ", "").isalpha():
        name=args.name.strip()
    else:
        print("Invalid Name")
        sys.exit(errno.EINVAL)

    # Check email
    pattern = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.match(pattern, args.email)):
        email=args.email
    else:
        print("Invalid email")
        sys.exit(errno.EINVAL)

    # Read and check password
    if not args.password:
        p1 = getpass(prompt='Password: ')
        p2 = getpass(prompt='Retype Password: ')
        if not p1==p2:
            print('Sorry, passwords do not match')
            sys.exit(errno.EINVAL)
        else: password=p1
    else:
        password = args.password

    if len(password) < 6:
        print('Password is too short - must be at least 6 characters')
        sys.exit(errno.EINVAL)

    # Create user
    with server.app_context():

        user = User.query.filter_by(email=email).first()
        if user:
            print('Email already exists.')
            sys.exit(errno.EINVAL)

        else:
            user = User(email=email,
                         first_name=name,
                         password=generate_password_hash(password,
                                                         method='sha256'
                                                        )
                       )
            db.create_all()
            db.session.add(user)
            db.session.commit()

            print(f'Account for {email} created!')
