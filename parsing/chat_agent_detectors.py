import re
from parsing.whatsapp import WhatsAppLineParser
from parsing.whatsapp_text_search_patterns import GENERAL_WA_SEARCH_PATTERN


class ChatAgentDetector(WhatsAppLineParser):

    def __init__(self, whatsapp_text, author_search_pattern):
        super(ChatAgentDetector, self).__init__(whatsapp_text)
        self.author_search_pattern = author_search_pattern

    def check_if_line_suitable_for_author_parse(self, line):
        # check if line is suitable
        desired_pattern = re.compile(self.author_search_pattern)
        return bool(desired_pattern.match(line))

    def get_participants_in_chat(self):
        list_of_lines = self.individual_lines_without_preamble
        authors_set = set()

        # iterate through lines of the whatsapp chat, getting authors as you go
        for text_line in list_of_lines:
            if len(text_line) == 0:
                continue

            # check if the line has the right format
            if self.check_if_line_suitable_for_author_parse(text_line):
                author_of_line = re.search(self.author_search_pattern,
                                           text_line).group(1)
                authors_set.add(author_of_line)

        list_of_authors = list(authors_set)
        if len(list_of_authors) == 0:
            return 'No detected participants'
        return list_of_authors


class WhatsAppChatAgentDetector(ChatAgentDetector):

    def __init__(self, whatsapp_text):
        super(WhatsAppChatAgentDetector, self).__init__(whatsapp_text, GENERAL_WA_SEARCH_PATTERN)
