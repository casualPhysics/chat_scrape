import re
from parsing.whatsapp import WhatsAppLineParser
from parsing.whatsapp_text_search_patterns import GENERAL_WA_SEARCH_PATTERN


class ChatSearchPatternVerifier(WhatsAppLineParser):

    def __init__(self, whatsapp_text, expected_search_pattern):
        super(ChatSearchPatternVerifier, self).__init__(whatsapp_text)
        self.expected_search_pattern = expected_search_pattern

    def verify_is_consistent_chat_pattern(self):
        """
        We need to check that the text follows a consistent
        text pattern
        """
        lines_of_text = self.individual_lines_without_preamble
        desired_pattern = re.compile(self.expected_search_pattern)
        if len(lines_of_text) == 0:
            return False
        for line in lines_of_text:
            if not bool(desired_pattern.match(line)):
                print(line)
                return False
        return True


class WhatsAppChatPatternVerifier(ChatSearchPatternVerifier):

    def __init__(self, whatsapp_text):
        super(WhatsAppChatPatternVerifier, self).__init__(whatsapp_text, GENERAL_WA_SEARCH_PATTERN)


class ChatFormVerifier(WhatsAppLineParser):

    def __init__(self, whatsapp_text):
        super(ChatFormVerifier, self).__init__(whatsapp_text)

    def verify_if_chat_belongs_to_types(self, possible_search_pattern_dictionary: dict) -> str:
        """
        Exported whatsapp chats come in different types,
        so we need to decide which one the chat text comes from.
        :param possible_search_pattern_dictionary: values are regex patterns.
        :return: key string of the type.
        """
        for pattern_source, search_pattern in possible_search_pattern_dictionary.items():
            chat_pattern_verifier = ChatSearchPatternVerifier(self.whatsapp_text, search_pattern)
            if chat_pattern_verifier.verify_is_consistent_chat_pattern():
                return pattern_source
        return "UNKNOWN CHAT TYPE"
