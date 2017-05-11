#!/usr/bin/python3
#praw 4.5.1

import praw
import pprint

from secrets import client_id, client_secret, password, user_agent, username

if __name__ == '__main__':

  r = praw.Reddit(client_id=client_id,
                  client_secret=client_secret,
                  user_agent=user_agent,
                  username=username,
                  password=password)

  pp = pprint.PrettyPrinter()

  #sub_modmail = input('Modmail subreddit: ')
  #modmail_id = input('Modmail id: ')

  sub_modmail = "askreddit"
  modmail_id = "x9ux"

  mail = r.subreddit(sub_modmail).modmail.__call__(id=modmail_id)

  print("Mail dict:")
  for attr in dir(mail._reddit):
    print("mail.%s = %s" % (attr, getattr(mail._reddit, attr)))

  print(mail.user)