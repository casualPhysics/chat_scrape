import pandas as pd
from collections import defaultdict
import re
import datetime
from pathlib import Path


class WhatsAppChatByteDecoder(object):

    def __init__(self, whatsapp_text):
        self.whatsapp_text = whatsapp_text
        self.decoded_text = self.decode_possible_bytes_object()

    def decode_possible_bytes_object(self):
        # convert from bytes to string
        if isinstance(self.whatsapp_text, (bytes, bytearray)):
            return self.whatsapp_text.decode()
        return self.whatsapp_text


class WhatsAppAgentDetector(WhatsAppChatByteDecoder):

    def __init__(self, whatsapp_text):
        super(WhatsAppAgentDetector, self).__init__(whatsapp_text)

    def get_participants_in_chat(self, text_delimiter, author_search_pattern):
        list_of_lines = self.decoded_text.split(text_delimiter)
        authors_set = set()

        # iterate through lines of the whatsapp chat, getting authors as you go
        for text_line in list_of_lines:
            if len(text_line) == 0:
                continue
            author_of_line = re.search(author_search_pattern,
                                       text_line).group(1)
            authors_set.add(author_of_line)
        list_of_authors = list(authors_set)
        if len(list_of_authors) == 0:
            return 'No detected participants'
        return list_of_authors


def parse_whatsapp_text_into_dataframe(raw_text, prompter, responder):
    result_dict = text_to_dictionary(raw_text, prompter, responder)
    df = pd.DataFrame.from_dict(result_dict).T[['prompt', 'completion']]
    return df


def converter(
        filepath: str,
        prompter: str,
        responder: str,
) -> pd.DataFrame:
    """
    Turn whatsapp chat data into a format
    that can be trained by openai's fine tuning api.
    :param file: Path to file we want to convert
    :param prompter: The person to be labelled as the prompter
    :param responder: The person to be labelled as the responder
    :return: a parsed pandas dataframe
    """

    with open(filepath, 'r') as fp:
        text = fp.read()

    df = parse_whatsapp_text_into_dataframe(text, prompter, responder)
    return df


def text_to_dictionary(text, prompt, response):

    # convert from bytes to string
    if isinstance(text, (bytes, bytearray)):
        text = text.decode()

    text_list = text.split('\n[')[1:]
    result_dict, count, prev_author = defaultdict(dict), 0, ''

    for ix, line in enumerate(text_list):

        result = re.sub('\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d:\d\d\]\s', '', line)
        author = re.match('(^.*?):', result)[1]
        message = re.match('.*:(.*)', result)[1]

        if author == prompt:
            if author == prev_author:
                prev = result_dict[count]['prompt']
                result_dict[count]['prompt'] = f"{prev}.{message}"
            else:
                count += 1
                result_dict[count].update({'prompt': message})

        elif author == response:
            if author == prev_author:
                prev = result_dict[count]['completion']
                result_dict[count]['completion'] = f"{prev}.{message}"
            else:
                result_dict[count].update({'completion': message})

        prev_author = author
    return result_dict


def construct_output_directory(output_name):
    Path(f"training/processed_files/{output_name}").mkdir(parents=True, exist_ok=True)


def construct_default_filename(prompter, responder):
    return f'output_{datetime.datetime.now()}_{prompter}_{responder}'


