from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from gmail_api.config import SCOPES


class GmailSessionServiceHandler(object):

    def __init__(self, gmail_cred_token_json):
        self.gmail_cred_token_json = gmail_cred_token_json

    def _get_credentials_object(self):
        return Credentials.from_authorized_user_info(self.gmail_cred_token_json, SCOPES)

    def get_service(self):
        return build('gmail', 'v1', credentials=self._get_credentials_object())
