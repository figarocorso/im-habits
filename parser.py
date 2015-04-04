import datetime
import re


class Parser(object):
    CONVERSATION_TIMEOUT = 3600  # seconds

    def __init__(self):
        self.lines = []
        self.conversations = []

    def word_list(self, phrase):
        return re.sub("[^\w]", " ",  phrase.lower()).split()

    @property
    def length(self):
        return len(self.lines)


class WhatsappParser(Parser):
    date = '(?P<day>[0-9]+)\/(?P<month>[0-9]+)\/(?P<year>[0-9]+) '
    time = '(?P<hour>[0-9]+)\:(?P<minute>[0-9]+)\:(?P<second>[0-9]+)\: '
    user = '(?P<user>.+?)\: '
    phrase = '(?P<phrase>.*)'

    regex_line = re.compile('^' + date + time + user + phrase + '$')

    def __init__(self, filename):
        super(WhatsappParser, self).__init__()

        with open(filename) as f:
            self.content = f.readlines()

        conversation = []
        for i in xrange(len(self.content)):
            line = self.content[i]
            group = self.regex_line.search(line)
            if not group:
                entry = self.lines[i - 1]
                entry['phrase'] = line
                entry['is_chain'] = True
            else:
                entry = {}
                for key, value in group.groupdict().iteritems():
                    entry[key] = value

            entry['words'] = self.word_list(entry['phrase'])
            self.lines.append(entry)

            if i != 0 and self._conversation_timeout(entry, self.lines[i - 1]):
                self.conversations.append(conversation)
                conversation = []
                conversation.append(entry)
            else:
                conversation.append(entry)

    def _conversation_timeout(self, entry, previous_entry):
        d1 = datetime.datetime(int(entry['year']), int(entry['month']),
                               int(entry['day']), int(entry['hour']),
                               int(entry['minute']))
        d2 = datetime.datetime(int(previous_entry['year']),
                               int(previous_entry['month']),
                               int(previous_entry['day']),
                               int(previous_entry['hour']),
                               int(previous_entry['minute']))

        delta_seconds = (d1 - d2).seconds

        return delta_seconds > self.CONVERSATION_TIMEOUT
