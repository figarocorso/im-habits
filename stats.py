import datetime


class Stats:
    def __init__(self, user):
        self.user = user
        self.number_of_lines = 0
        self.number_of_words = 0
        self.number_of_chains = 0
        self.forever_alone = 0
        self.conversations = 0
        self.phrases = {}
        self.dictionary = {}
        self.weekday = {}
        self.friendship = {}

    def __str__(self):
        # TODO: Implement?
        return "Number of lines : %d" % self.number_of_lines

    def __repr__(self):
        return self.__str__()

    def add_line(self, line):
        self.number_of_lines += 1
        self.number_of_words += len(line['words'])
        self._add_words(line['words'])
        self._add_phrase(int(line['year']), int(line['month']),
                         int(line['day']), int(line['hour']), line['phrase'])

    def add_conversation_users(self, users):
        self.conversations += 1

        if len(users) == 1:
            self.forever_alone += 1
            return

        for user in users:
            self._add_friendship(user)

    def _add_friendship(self, user):
        try:
            self.friendship[user] += 1
        except KeyError:
            self.friendship[user] = 1

    def add_conversation(self):
        self.conversations += 1

    def _add_words(self, words):
        for word in words:
            try:
                self.dictionary[word] += 1
            except KeyError:
                self.dictionary[word] = 1

    def _add_phrase(self, year, month, day, hour, phrase):
        if year not in self.phrases:
            self.phrases[year] = {}
            self.phrases[year]['count'] = 0
        if month not in self.phrases[year]:
            self.phrases[year][month] = {}
            self.phrases[year][month]['count'] = 0
        if day not in self.phrases[year][month]:
            self.phrases[year][month][day] = {}
            self.phrases[year][month][day]['count'] = 0
        if hour not in self.phrases[year][month][day]:
            self.phrases[year][month][day][hour] = {}
            self.phrases[year][month][day][hour]['count'] = 0
            self.phrases[year][month][day][hour]['phrases'] = []

        self.phrases[year]['count'] += 1
        self.phrases[year][month]['count'] += 1
        self.phrases[year][month][day]['count'] += 1
        self.phrases[year][month][day][hour]['count'] += 1
        self.phrases[year][month][day][hour]['phrases'].append(phrase)

        weekday = datetime.datetime(year, month, day).weekday()
        try:
            self.weekday[weekday] += 1
        except KeyError:
            self.weekday[weekday] = 1
