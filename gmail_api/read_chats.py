from __future__ import print_function

import argparse
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from attachments import get_attachments
from utils import write_bytes_file
from config import WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY
from utils import unzip_files_in_dir_to_dir

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


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


def download_email_attachments(creds, filter_string, user_id, destination_path):
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    messages = service.users().messages().list(userId=user_id, q=filter_string).execute()

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

    main(WHATSAPP_DATA_FILTER, MY_USER_ID, TRAINING_DIRECTORY)
    # unzip_files_in_dir_to_dir('../family_chats/zips', '../family_chats/text')
