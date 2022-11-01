from __future__ import print_function

import argparse
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gmail_api.attachments import get_attachments
from gmail_api.utils import write_bytes_file, unzip_files_in_dir_to_dir
from gmail_api.config import WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY, GMAIL_API_TOKEN_DIRECTORY



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


def get_email_message_objects(gmail_cred_token_json, user_id: str, filter_string: str):
    """
    :param gmail_cred_token_json: The token json that can be loaded in session.
    :param user_id: 'me' for default works.
    :param filter_string: Filtering criteria for the
    :return: service, messages
    """
    service = build('gmail', 'v1', credentials=gmail_cred_token_json)
    messages = service.users().messages().list(userId=user_id, q=filter_string).execute()
    return service, messages


def iterate_through_message_objects(gmail_cred_token, user_id, filter_string, func):
    service, messages = get_email_message_objects(gmail_cred_token, filter_string, user_id)
    if len(messages) == 0: raise Exception('No messages to iterate through with current filters.')
    item_store =
    for message in messages:
        func(service, message)


def get
def get_attachment_name_from_message(message, service):
    pass


def
def get_message_details(message):
    pass



# def download_email_attachments(creds, filter_string, user_id, destination_path):
#     for message in messages["messages"]:
#         message_id = message["id"]
#         attachment, name = get_attachments(service, user_id, message_id)
#         target = destination_path + name
#         write_bytes_file(target, attachment)


def upload_email_attachments():
    pass


def summarise_email_attachments():
    pass


def list_emails_from_filter(creds, filter_string, user_id):
    messages = get_email_message_objects(creds, filter_string, user_id)

    for message in messages["messages"]:
        message_id = message["id"]
        attachment, name = get_attachments(service, user_id, message_id)
        target = destination_path + name
        write_bytes_file(target, attachment)


def gcloud_store_email_attachments():
    pass


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
    print(get_email_message_objects(creds, MY_USER_ID, WHATSAPP_DATA_FILTER))

    # main(WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY)

    # unzip_files_in_dir_to_dir('../family_chats/zips', '../family_chats/text')
