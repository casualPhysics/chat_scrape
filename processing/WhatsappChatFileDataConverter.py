import pathlib
from gmail_api.utils import read_txt_file_from_zip_buffer


class WhatsAppChatFileDataConverter(object):
    def __init__(self, whatsapp_data_buffer, filename):
        self.whatsapp_data_buffer = whatsapp_data_buffer
        self.filename = filename

    def get_chat_string_from_file(self):
        attachment_file_type = pathlib.Path(self.filename).suffix

        # handle the case when the attachment data is a zip file
        if attachment_file_type == '.zip':
            text = read_txt_file_from_zip_buffer(self.whatsapp_data_buffer)
        # whatsapp texts may just return a txt file
        elif attachment_file_type == '.txt':
            text = self.whatsapp_data_buffer
        else:
            raise Exception('The attachment is not .txt')

        # convert between bytes array and text
        if isinstance(text, (bytes, bytearray)):
            return text.decode("utf-8")
        if isinstance(text, str):
            return text
        else:
            raise Exception('The unzipped file is not of string type. ')
