#!/usr/bin/python

import re
import datetime


date = '(?P<day>[0-9]+)\/(?P<month>[0-9]+)\/(?P<year>[0-9]+) '
time = '(?P<hours>[0-9]+)\:(?P<minutes>[0-9]+)\:(?P<seconds>[0-9]+)\: '
user = '(?P<user>.+?)\: '
phrase = '(?P<phrase>.*)'

regex_line = re.compile('^' + date + time + user + phrase + '$')


def increase_chain(user, stats):
    if 'chain' not in stats:
        stats['chain'] = {}
    if 'global' not in stats['chain']:
        stats['chain']['global'] = 0
    if user not in stats['chain']:
        stats['chain'][user] = 0

    stats['chain'][user] += 1
    stats['chain']['global'] += 1


def count_phrases(user, stats):
    if 'number' not in stats:
        stats['number'] = {}

    if 'global' not in stats['number']:
        stats['number']['global'] = 0
    if user not in stats['number']:
        stats['number'][user] = 0

    stats['number']['global'] += 1
    stats['number'][user] += 1


def add_user_stat(user, stat, stat_value, stats):
    if stat not in stats:
        stats[stat] = {}

    if 'global' not in stats[stat]:
        stats[stat]['global'] = {}
    if user not in stats[stat]:
        stats[stat][user] = {}

    if stat_value not in stats[stat]['global']:
        stats[stat]['global'][stat_value] = 0
    if stat_value not in stats[stat][user]:
        stats[stat][user][stat_value] = 0

    stats[stat]['global'][stat_value] += 1
    stats[stat][user][stat_value] += 1


def count_phrases_by_hour(user, hour, stats):
    add_user_stat(user, 'hour', hour, stats)


def count_phrases_by_month(user, month, stats):
    add_user_stat(user, 'month', month, stats)


def count_phrases_by_year(user, year, stats):
    add_user_stat(user, 'year', year, stats)


def count_phrases_by_friendship(user, previous_user, stats):
    if previous_user and user != previous_user:
        add_user_stat(user, 'friendship_raw', previous_user, stats)


def count_phrases_by_weekday(user, year, month, day, stats):
    weekday = datetime.datetime(int(year), int(month), int(day)).weekday()
    add_user_stat(user, 'weekday', weekday, stats)


def count_words(user, phrase, stats):
    word_list = re.sub("[^\w]", " ",  phrase.lower()).split()
    for word in word_list:
        add_user_stat(user, 'words', word, stats)


def get_raw_stats(content):
    stats = {}
    previous_group = None
    previous_user = ""
    for line in content:
        group = regex_line.search(line)

        if not group:
            group = previous_group
            phrase = line
            increase_chain(group.groupdict()['user'], stats)
        else:
            phrase = group.groupdict()['phrase']

        parsed_string = group.groupdict()
        user = parsed_string['user']

        count_phrases(user, stats)
        count_phrases_by_hour(user, parsed_string['hours'], stats)
        count_phrases_by_weekday(user, parsed_string['year'],
                                 parsed_string['month'], parsed_string['day'],
                                 stats)
        count_phrases_by_month(user, parsed_string['month'], stats)
        count_phrases_by_year(user, parsed_string['year'], stats)
        count_phrases_by_friendship(user, previous_user, stats)

        count_words(user, phrase, stats)

        previous_group = group
        previous_user = user

    return stats


def display_stats(stats):
    for key, value in stats.iteritems():
        print key
        print value
        print

    print
    print "Global words"
    for word, count in stats['words']['global'].iteritems():
        if count > 150:
            print "%s: %d" % (word, int(count))

    print
    print "Talking hours"
    for hour, count in stats['hour']['global'].iteritems():
        print "%s: %d" % (hour, int(count))


if __name__ == "__main__":
    fname = 'whatsapp/vacas-whatsapp.log'
    with open(fname) as f:
        content = f.readlines()

    stats = get_raw_stats(content)
    display_stats(stats)
