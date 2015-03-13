# Piazza bot
# Created by Joel Choo

# For Google App Engine to detect external modules (piazza_api module)
import sys
sys.path.insert(0, 'lib')

import random
from settings import *
from piazza_api import Piazza
from google.appengine.api import mail

def main():
    # Logging into Piazza instance
    p = Piazza()
    p.user_login(email= PIAZZA_EMAIL, password=PIAZZA_PASSWORD)

    # Accessing the class and getting most recent posts
    cls = p.network(PIAZZA_CLASS_ID)
    posts = cls.iter_all_posts(limit=POSTS_TO_CHECK)

    unanswered = 0
    for post in posts:
        if not post_answered(post):
            unanswered += 1

    sender = '%s <%s>' % (BOT_EMAIL, BOT_EMAIL)
    subject = 'Piazza Alert!! There are %d unanswered questions right now!' % unanswered
    body = '''
Hi! There are %d unanswered questions on Piazza right now! Get to it!
''' % unanswered

    # Debug mode on, send emails to debug mailing list
    if DEBUG:
        for email in DEBUG_MAILING_LIST:
            mail.send_mail(sender, email, subject, body)

    # If number of unanswered questions exceeds the threshold, shoot some emails
    elif unanswered > THRESHOLD:
        random.shuffle(MAILING_LIST)
        the_chosen_ones = MAILING_LIST[:unanswered]
        for email in the_chosen_ones:
            mail.send_mail(sender, email, subject, body)

    return

def post_answered(post):
    try:
        if 'questions' not in post['folders']:
            return True
        for change in post['change_log']:
            if change['type'] == 'i_answer':
                return True
        return False
    except:
        return True

if __name__ == '__main__':
    main()
