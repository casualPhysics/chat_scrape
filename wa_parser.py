import pandas as pd
from collections import defaultdict
import re
import argparse
import datetime


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

def get_delimiters():
    """
    This function should scan the dataframe 
    for unused delimiters in the 
    dataframe
    """
    return 0

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process your whatsapp chat data.')
    parser.add_argument('path', type=str, help='Path to file')
    parser.add_argument('prompter', type=str, help='Name of Prompter')
    parser.add_argument('responder', type=str, help='Name of Responder')

    args = parser.parse_args()
    path = args.path
    prompter = args.prompter
    responder = args.responder

    converter(path, prompter, responder).to_csv(f'output_{datetime.datetime.now()}.csv')
