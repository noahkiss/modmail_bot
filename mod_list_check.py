#!/usr/bin/python3

import praw

from secrets import client_id, client_secret, password, user_agent, username, main_sub, modmail_sub, backroom_sub
try:
  from secrets import unban_sub
except ImportError:
  unban_sub = False

r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password)

if unban_sub != False:
  unban_sub  = r.subreddit(unban_sub)
main_sub     = r.subreddit(main_sub)
modmail_sub  = r.subreddit(modmail_sub)
backroom_sub = r.subreddit(backroom_sub)

if __name__ == '__main__':
  moderators = []
  for mod in main_sub.moderator():
    if 'all' in mod.mod_permissions or 'mail' in mod.mod_permissions:
      try:
        modmail_sub.contributor.add(mod.name)
      except:
        pass
      try: 
        unban_sub.contributor.add(mod.name)
      except:
        pass
      try: 
        backroom_sub.contributor.add(mod.name)
      except:
        pass