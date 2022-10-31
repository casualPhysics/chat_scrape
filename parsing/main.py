import argparse
import datetime
from parsing.whatsapp import converter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process your whatsapp chat data.')
    parser.add_argument('path', type=str, help='Path to file')
    parser.add_argument('prompter', type=str, help='Name of Prompter')
    parser.add_argument('responder', type=str, help='Name of Responder')
    parser.add_argument('-filename', type=str, help='Destination filename')

    args = parser.parse_args()
    path = args.path
    prompter = args.prompter
    responder = args.responder
    filename = args.filename

    save_file = filename if filename else datetime.datetime.now()
    converter(path, prompter, responder).to_csv(f'output_{save_file}.csv')

