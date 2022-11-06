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
            return read_txt_file_from_zip_buffer(self.whatsapp_data_buffer)

        if attachment_file_type == '.txt':
            return self.whatsapp_data_buffer
