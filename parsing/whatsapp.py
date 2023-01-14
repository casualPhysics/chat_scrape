import pandas as pd
from collections import defaultdict
import re
import datetime
from pathlib import Path
from parsing.whatsapp_text_search_patterns import LINE_SPLIT_DELIMITER, GENERAL_WA_MULTI_SEARCH_PATTERN


class WhatsAppChatByteDecoder(object):

    def __init__(self, whatsapp_text):
        self.whatsapp_text = whatsapp_text
        self.decoded_text = self.decode_possible_bytes_object()

    def decode_possible_bytes_object(self):
        # convert from bytes to string
        if isinstance(self.whatsapp_text, (bytes, bytearray)):
            return self.whatsapp_text.decode()
        return self.whatsapp_text


class WhatsAppLineParser(WhatsAppChatByteDecoder):

    def __init__(self, whatsapp_text):
        super(WhatsAppLineParser, self).__init__(whatsapp_text)
        self._individual_lines = self.get_split_lines()
        self.individual_lines_without_preamble = ""
        self.remove_trailing_empty_strings()
        self.set_individual_lines_without_preamble()

    def get_split_lines(self):
        return self.decoded_text.split(LINE_SPLIT_DELIMITER)

    def remove_trailing_empty_strings(self):
        self._individual_lines = list(filter(lambda x: x != '', self._individual_lines))
        return self

    def remove_preamble_from_whatsapp_lines(self):
        whatsapp_preamble_text = "Messages and calls are end-to-end encrypted."
        filtered_text_lines = []
        for text_line in self._individual_lines:
            if whatsapp_preamble_text not in text_line:
                filtered_text_lines.append(text_line)
        return filtered_text_lines

    def set_individual_lines_without_preamble(self):
        self.individual_lines_without_preamble = self.remove_preamble_from_whatsapp_lines()
        return self

    def get_individual_lines_without_preamble(self):
        return self.individual_lines_without_preamble


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


def get_text_lines_from_chat(text: str) -> list:
    """
    Get lines of text from a whatsapp chat
    :param text:
    :return:
    """
    # convert from bytes to string
    if isinstance(text, (bytes, bytearray)):
        text = text.decode()

    text_list = text.split('\n')[1:]
    if len(text_list) == 0:
        raise Exception('No detected lines in this script.')
    return text_list


def extract_dates_in_chat(text):
    """
    Extract dates from a particular whatsapp chat.
    :param text: The data to analyse
    :return:
    """
    if not isinstance(text, (str, bytes, bytearray)):
        raise ValueError("Input must be a string or bytes-like object.")

    if isinstance(text, (bytes, bytearray)):
        text = text.decode()

    pattern = r"\d{2}/\d{2}/\d{4}"
    dates = re.findall(pattern, text)

    # we may not return any results.
    if len(dates) == 0:
        print(f'No text with dates of the format {pattern}.')
        return None

    return list(set(dates))


def extract_text_spoken_by_author(text: str, selected_author: str, lazy_select=True):
    """
    We would like to isolate lines of text associated with a specific author,
    so that we can match their style of speech later on.
    :param text: The full whatsapp text.
    :param selected_author: The author we want to extract the text from.
    :param lazy_select: This searches for a case-insensitive, subset from the author. This
    is a fuzzy string match.
    :return:
    """

    text_lines = []
    for ix, line in enumerate(get_text_lines_from_chat(text)):

        # check if we have a valid whatsapp search pattern
        search_pattern = re.search(GENERAL_WA_MULTI_SEARCH_PATTERN, line)
        if search_pattern is not None:

            author = search_pattern.group(1)
            message = search_pattern.group(2)

            if lazy_select:
                if selected_author.lower() in author.lower():
                    text_lines.append(message)
            else:
                if author == selected_author:
                    text_lines.append(message)

    # we may not return any results.
    if len(text_lines) == 0:
        return 'No text lines with requested author. '

    return text_lines


def text_to_dictionary(text, prompt, response):
    """
    We convert a whatsapp chat into a prompt and
    response dataframe for the purposes of finetuning.
    :param text:
    :param prompt:
    :param response:
    :return:
    """
    # convert from bytes to string
    if isinstance(text, (bytes, bytearray)):
        text = text.decode()

    text_list = text.split('\n')[1:]
    result_dict, count, prev_author = defaultdict(dict), 0, ''
    for ix, line in enumerate(text_list):
        search_pattern = re.search(GENERAL_WA_MULTI_SEARCH_PATTERN, line)
        if search_pattern is not None:
            author = search_pattern.group(1)
            message = search_pattern.group(2)
        else:
            continue
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


from family_chats.style_prompt import AFIQ_STYLE_PROMPT
print( extract_dates_in_chat(AFIQ_STYLE_PROMPT) )