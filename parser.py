import re


class Parser(object):
    def __init__(self):
        self.lines = []

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

        previous_entry = {}
        for line in self.content:
            group = self.regex_line.search(line)
            if not group:
                entry = previous_entry
                entry['phrase'] = line
                entry['is_chain'] = True
            else:
                entry = {}
                for key, value in group.groupdict().iteritems():
                    entry[key] = value

            entry['words'] = self.word_list(entry['phrase'])
            self.lines.append(entry)
            previous_entry = entry
