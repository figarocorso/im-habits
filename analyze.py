from parser import WhatsappParser
from stats import Stats


def display_stats(stats):
    for key, value in stats.iteritems():
        print key
        print value
        print


if __name__ == "__main__":
    fname = 'whatsapp/vacas-whatsapp.log'
    data = WhatsappParser(fname)

    user_stats = {'global': Stats('global')}
    for line in data.lines:
        user = line['user']
        if user not in user_stats:
            user_stats[user] = Stats(user)

        user_stats['global'].add_line(line)
        user_stats[user].add_line(line)

    for conversation in data.conversations:
        users_involved = []
        for line in conversation:
            if line['user'] not in users_involved:
                users_involved.append(line['user'])

        for user in users_involved:
            user_stats[user].add_conversation_users(users_involved)

        user_stats['global'].add_conversation()

        last_word_user = conversation[-1]['user']
        user_stats[last_word_user].add_last_word()
