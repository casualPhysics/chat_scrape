import pandas as pd
from collections import defaultdict
import re
import argparse
import datetime
import os
from pathlib import Path


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
    text_list = text.split('\n[')[1:]
    result_dict, count, prev_author = defaultdict(dict), 0, ''
    for ix, line in enumerate(text_list):

        result = re.sub(r'\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d:\d\d\]\s', '', line)
        author = re.match('(^.*?):', result)[1]
        message = re.match('.*:(.*)', result)[1]

        if author == prompter:
            if author == prev_author:
                prev = result_dict[count]['prompt']
                result_dict[count]['prompt'] = f"{prev}.{message}"
            else:
                count += 1
                result_dict[count].update({'prompt' : message})

        elif author == responder:
            if author == prev_author:
                prev = result_dict[count]['completion']
                result_dict[count]['completion'] = f"{prev}.{message}"
            else:
                result_dict[count].update({'completion' : message})

        prev_author = author
    df = pd.DataFrame.from_dict(result_dict).T[['prompt', 'completion']]
    return df


def construct_output_directory(output_name):
    Path(f"training/processed_files/{output_name}").mkdir(parents=True, exist_ok=True)


def construct_default_filename(prompter, responder):
    return f'output_{datetime.datetime.now()}_{prompter}_{responder}'


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process your whatsapp chat data.')
    parser.add_argument('path', type=str, help='Path to file')
    parser.add_argument('prompter', type=str, help='Name of Prompter')
    parser.add_argument('responder', type=str, help='Name of Responder')
    parser.add_argument('-filename', type=str, help='Destination filename' )

    args = parser.parse_args()
    path = args.path
    prompter = args.prompter
    responder = args.responder
    filename = args.filename

    save_file = filename if filename else datetime.datetime.now()
    converter(path, prompter, responder).to_csv(f'output_{save_file}.csv')


