from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from routes.register_email_taps import db
from flask import session, url_for
import json
from main_app import app


def get_email_user_name():
    service = build('gmail', 'v1',
                    credentials=Credentials.from_authorized_user_info(json.loads(session['email_token'])))
    return service.users().getProfile(userId='me').execute()


def save_email_labels():
    # Initialize the Gmail API client
    creds = Credentials.from_authorized_user_info(json.loads(session['email_token']),
                                                  scopes=['https://www.googleapis.com/auth/gmail.readonly'])
    service = build('gmail', 'v1', credentials=creds)

    # Get the user's email address
    user_profile = service.users().getProfile(userId='me').execute()
    user_email = user_profile['emailAddress']

    # Get a reference to the "emails" collection in Firestore
    emails_ref = db.collection('emails')

    # Get the list of labels for the user's account
    labels = service.users().labels().list(userId='me').execute()
    print(labels)
    return labels


def get_labeled_email_attachments(label_id):
    creds = Credentials.from_authorized_user_info(json.loads(session['email_token']))
    service = build('gmail', 'v1', credentials=creds)

    attachments = []

    # Get the list of messages with the specified label
    messages = service.users().messages().list(userId='me', labelIds=[label_id]).execute()

    # Loop through the messages and get their attachments
    for message in messages['messages']:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()

        # If the message has any attachments, loop through them and store their
        # filename, size, and MIME type in the attachments list
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if 'filename' in part:
                    if 'attachmentId' in part['body']:
                        attachment = {
                            'filename': part['filename'],
                            'mimeType': part['mimeType'],
                            'attachmentId': part['body']['attachmentId'],
                        }
                        attachments.append(attachment)

                        doc_ref = (
                            db.collection(
                                f"users/prototype_users/{session['user_email_key']}/{get_email_user_name()}/{label_id}/")
                            .document(attachment['filename'])
                        )
                        doc_ref.set(attachment)
    return url_for('index')


def cache_label():
    pass


@app.route('/retrieve_emails_from_label/<label>')
def retrieve_emails_from_label(label):
    session['labelled_email_attachments'] = [item['filename'] for item in get_labeled_email_attachments(label)]
    return url_for('index')

    # for label in labels:
    #     label_name = label['id']
    #
    #     # Get the list of emails with this label
    #     label_id = label['id']
    #     messages = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
    #
    #     # Iterate over the emails and save them to Firestore
    #     for message in messages:
    #         # Get the email details
    #         msg = service.users().messages().get(userId='me', id=message['id']).execute()
    #
    #         print(msg)
    #         # Save the email to Firestore
    #         # email_ref = emails_ref.document()
    #         # email_ref.set({
    #         #     'user': user_email,
    #         #     'label': label_name,
    #         #     'details': msg
    #         # })
