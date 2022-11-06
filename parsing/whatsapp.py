import pandas as pd
from collections import defaultdict
import re
import datetime
from pathlib import Path


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
    text_list = text.split('\n[')[1:]
    result_dict, count, prev_author = defaultdict(dict), 0, ''
    for ix, line in enumerate(text_list):

        result = re.sub(r'\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d:\d\d\]\s', '', line)
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


