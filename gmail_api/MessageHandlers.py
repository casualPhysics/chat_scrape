from googleapiclient.discovery import build
from gmail_api.config import WHATSAPP_DATA_FILTER, MY_USER_ID


class GmailMessageHandler(object):

    def __init__(self, gmail_cred_token, user_id, filter_string):
        self.gmail_cred_token = gmail_cred_token
        self.user_id = user_id
        self.filter_string = filter_string

    def get_service(self):
        return build('gmail', 'v1', credentials=self.gmail_cred_token)

    def get_message_collection(self):
        return self.get_service().users().messages().list(userId=self.user_id, q=self.filter_string).execute()

    def get_message_ids(self):
        return [message["id"] for message in self.get_message_collection()]


class UserGmailMessageHandler(GmailMessageHandler):

    def __init__(self, gmail_cred_token, filter_string):
        super(UserGmailMessageHandler, self).__init__(gmail_cred_token, MY_USER_ID, filter_string)


class WhatsAppDataGmailMessageHandler(UserGmailMessageHandler):

    def __init__(self, gmail_cred_token):
        super(WhatsAppDataGmailMessageHandler, self).__init__(gmail_cred_token, WHATSAPP_DATA_FILTER)
