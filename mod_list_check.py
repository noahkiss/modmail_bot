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
  sub_unban  = r.subreddit(unban_sub)
sub_main     = r.subreddit(main_sub)
sub_modmail  = r.subreddit(modmail_sub)
sub_backroom = r.subreddit(backroom_sub)

if __name__ == '__main__':
  moderators = []
  for mod in sub_main.moderator():
    if 'all' in mod.mod_permissions or 'mail' in mod.mod_permissions:
      try:
        sub_modmail.contributor.add(mod.name)
      except:
        pass
      try: 
        sub_unban.contributor.add(mod.name)
      except:
        pass
      try: 
        sub_backroom.contributor.add(mod.name)
      except:
        pass
