import json
import pathlib

from flask import Flask
from flask import redirect, url_for, render_template
from flask import request
from flask import session

import session_config as sc
from gmail_api.MessageHandlers import WhatsAppDataGmailMessageHandler
from gmail_api.attachments import get_attachments
from gmail_api.config import GMAIL_API_CREDENTIALS
from gmail_api.handler import get_user_token

from parsing.whatsapp import parse_whatsapp_text_into_dataframe
from processing.WhatsappChatDisplayHandler import WhatsAppChatDisplayHandler
from processing.WhatsappChatFileDataConverter import WhatsAppChatFileDataConverter

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    """
    The index page should show whether the user is logged in
    :return:
    """
    email_status = 'Email' if sc.EMAIL_TOKEN_KEY in session else 'No Email'
    session_items = session.keys()
    name = 'Afiq'

    return render_template('home/index.html', segment='index', name=session['email_token'])


@app.route('/email_registry')
def email_registry():
    if sc.EMAIL_TOKEN_KEY in session:
        return f'Token already exists {session[sc.EMAIL_TOKEN_KEY]}'
    else:
        creds = None
        token = get_user_token(creds, GMAIL_API_CREDENTIALS)
        session['email_token'] = token
    redirect(url_for('index'))


@app.route('/refresh_session')
def refresh_session():
    del session[sc.EMAIL_TOKEN_KEY]
    return url_for('index')


@app.route('/attachments', methods=['POST', 'GET'])
def attachments():
    if 'email_token' not in session: return "Email not configured for training data"

    whatsapp_message_handler = WhatsAppDataGmailMessageHandler(
        json.loads(session[sc.EMAIL_TOKEN_KEY])
    )

    # show snippets of each whatsapp message available to pretrain on
    message_packet_data_by_ids = {}
    full_whatsapp_texts_by_ids = {}
    whatsapp_data_message_ids = whatsapp_message_handler.get_list_of_message_ids()

    # we assign the raw text to html
    for message_id_string in whatsapp_data_message_ids:

        # get the raw file data from attachments, by ids
        file_data, name = get_attachments(
            whatsapp_message_handler.get_service(),
            whatsapp_message_handler.get_user_id,
            message_id_string
        )

        # get the whatsapp string from email
        whatsapp_text_string = (
            WhatsAppChatFileDataConverter(file_data, name)
            .get_chat_string_from_file()
        )

        whatsapp_display_text_dictionary = {
            'name': name,
            'display_text': WhatsAppChatDisplayHandler()
        }

        # index and store the full texts by message id
        full_whatsapp_texts_by_ids[message_id_string] = whatsapp_text_string
        message_packet_data_by_ids[message_id_string] = whatsapp_display_text_dictionary

        # create dictionaries that store button data
        parsing_button_dictionary = {'button_name': f'button that parses chat data',
                                     'button_value': f'parsing button id: {message_id_string}'}

        message_packet_data_by_ids[message_id_string].update(parsing_button_dictionary)

    if request.method == 'POST':


        parse_whatsapp_text_into_dataframe()
    return render_template('home/attachments.html', message_packets=message_packet_data_by_ids)


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
