from __future__ import print_function

import argparse
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

from gmail_api.attachments import get_attachments
from gmail_api.utils import write_bytes_file, unzip_files_in_dir_to_dir
from gmail_api.config import WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY, GMAIL_API_TOKEN_DIRECTORY
from gmail_api.authentication.gmail_credentials_for_user import get_user_token_for_gmail_api, read_token_from_path


def main(filter_string, user_id, destination_path):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        download_email_attachments(creds, filter_string, user_id, destination_path)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


class MessageCollection(object):
    def __init__(self, service, messages, user_id):
        self.service = service
        self.messages = messages
        self.user_id = user_id

    def iterate_through_message_objects(self, func):
        item_store = []
        for message in self.messages:
            message_id = message['id']
            item_store.append(func(message_id, self.service, self.user_id))
        return item_store

    def get_message_ids(self):
        return 0


# this class should be an email collection object
def iterate_through_message_objects(gmail_cred_token, user_id, filter_string, func):
    service, messages = get_email_message_objects(gmail_cred_token, filter_string, user_id)
    if len(messages) == 0: raise Exception('No messages to iterate through with current filters.')


def _get_attachment_name_from_message(message_id, service, user_id):
    attachment, name = get_attachments(service, user_id, message_id)
    return name


def _get_attachment_file_from_message(message_id, service, user_id):
    attachment, name = get_attachments(service, user_id, message_id)
    return attachment


def list_emails_from_filter(creds, filter_string, user_id):
    messages = get_email_message_objects(creds, filter_string, user_id)

    for message in messages["messages"]:
        message_id = message["id"]
        attachment, name = get_attachments(service, user_id, message_id)
        target = destination_path + name
        write_bytes_file(target, attachment)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Desktop download email attachments')
    # parser.add_argument('-id')
    # parser.add_argument('-destination_path', type=str, help='Path to file')
    # parser.add_argument('-filters', type=str, help='Name of Prompter')
    #
    # args = parser.parse_args()
    # id = args.path
    # prompter = args.prompter
    # responder = args.responder
    # filename = args.filename
    creds = read_token_from_path(GMAIL_API_TOKEN_DIRECTORY)
    messages, service = get_email_message_objects(creds, MY_USER_ID, WHATSAPP_DATA_FILTER)
    iterate_through_message_objects

    # main(WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY)

    # unzip_files_in_dir_to_dir('../family_chats/zips', '../family_chats/text')
