import base64
from apiclient import errors
import zipfile


def get_attachments(service, user_id, msg_id):
    """Get and store attachment from Message with given id.

    :param service: Authorized Gmail API service instance.
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param msg_id: ID of Message containing attachment.
    """
    global file_data, name
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if part['filename']:
                if 'data' in part['body']:
                    data = part['body']['data']
                else:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id,
                                                                       id=att_id).execute()
                    data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                name = part['filename']
        return file_data, name

    except errors.HttpError as error:
        print(f'An error occurred: {error}')
