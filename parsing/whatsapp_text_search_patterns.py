# This regex pattern finds the author in a general whatsapp chat line
# There is the use of a lzy operator, denoted by a question mark in the brackets.

GENERAL_WA_SEARCH_PATTERN = r".*\[?\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d:?\d?\d?\]?\s?-? (.*?):.*"
GENERAL_WA_MULTI_SEARCH_PATTERN = r'\[?\d\d\/\d\d\/\d\d\d\d, \d\d:\d\d:?\d?\d?\]?\s?-? (.*?):(.*)'
LINE_SPLIT_DELIMITER = "\n"
