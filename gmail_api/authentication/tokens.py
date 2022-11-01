from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_user_token(credentials, client_secret_file_path):
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        return credentials.to_json()


def read_token_from_path(path_to_token: str):
    if os.path.exists(path_to_token):
        token_json = Credentials.from_authorized_user_file(path_to_token, SCOPES)
    return token_json


def read_token_from_session(session):
    if 'token' not in session.keys():
        raise Exception('Token does not exist')
    return session['token']
