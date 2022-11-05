from gmail_api.config import WHATSAPP_DATA_FILTER, MY_USER_ID
from gmail_api.ServiceHandler import GmailSessionServiceHandler


class GmailMessageHandler(GmailSessionServiceHandler):

    def __init__(self, gmail_cred_token_json, user_id, filter_string):
        super(GmailMessageHandler, self).__init__(gmail_cred_token_json)
        """
        This interface manages messages that belong to a particular user. 
        """
        self.gmail_cred_token_json = gmail_cred_token_json
        self.user_id = user_id
        self.filter_string = filter_string

    @property
    def get_user_id(self):
        return self.user_id

    def get_message_collection(self):
        return self.get_service().users().messages().list(userId=self.user_id, q=self.filter_string).execute()

    def get_list_of_message_ids(self):
        """
        Each message Id has a string
        :return: List of ids
        """
        return [message["id"] for message in self.get_message_collection()['messages']]


class MyUserGmailMessageHandler(GmailMessageHandler):

    def __init__(self, gmail_cred_token, filter_string):
        super(MyUserGmailMessageHandler, self).__init__(gmail_cred_token, MY_USER_ID, filter_string)


class WhatsAppDataGmailMessageHandler(MyUserGmailMessageHandler):

    def __init__(self, gmail_cred_token):
        super(WhatsAppDataGmailMessageHandler, self).__init__(gmail_cred_token, WHATSAPP_DATA_FILTER)

