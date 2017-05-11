#!/usr/bin/python3

import praw

from secrets import client_id, client_secret, password, user_agent, username, main_sub, modmail_sub

r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password)

sub_main     = r.subreddit(main_sub)
sub_modmail  = r.subreddit(modmail_sub)

if __name__ == '__main__':
  moderators = []
  contributors = []

  mods = sub_main.moderator()
  approved = sub_modmail.contributor()

  for mod in mods:
    if 'all' in mod.mod_permissions or 'mail' in mod.mod_permissions:
      moderators.append(mod.name)

  for contributor in approved:
    contributors.append(contributor.name)

  for user in moderators:
    if user not in contributors:
      sub_modmail.contributor.add(user)
      print("Adding " + user + " to " + modmail_sub)

  for user in contributors:
    if user not in moderators:
      sub_modmail.contributor.remove(user)
      print("Removing " + user + " from " + modmail_sub)