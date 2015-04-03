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

    user_stats = {'global': Stats()}
    for i in xrange(data.length):
        line = data.lines[i]
        user = line['user']
        if user not in user_stats:
            user_stats[user] = Stats()

        user_stats['global'].add_line(line)
        user_stats[user].add_line(line)
