from flask import session
from flask import Flask
from flask import request
from flask import redirect, url_for, render_template

import sys
from gmail_api.handler import get_user_token
from gmail_api.config import GMAIL_API_CREDENTIALS


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    """
    The index page should show whether the user is logged in
    :return:
    """
    email_status = 'Email' if 'email_token' in session else 'No Email'
    session_items = session.keys()
    name = 'Afiq'

    return render_template('home/index.html', segment='index', name=session['email_token'])


@app.route('/email_registry')
def email_registry():
    if 'email_token' in session:
        return f'Token already exists {session["email_token"]}'
    else:
        creds = None
        token = get_user_token(creds, GMAIL_API_CREDENTIALS)
        session['email_token'] = token
    redirect(url_for('index'))


@app.route('/email', methods=['GET', 'POST'])
def sign_in_email():
    if request.method == 'POST':
        session['credentials'] = 'hi'
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
