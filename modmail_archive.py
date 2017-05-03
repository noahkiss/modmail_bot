#!/usr/bin/python3

'''
read modmail
  new modmail?
    add id to db, make post in modmail sub, add username to user column, save post id link
  old mail?
    find id in db, update post in modmail sub (under x chars - 10000?), add number for each mod who answered
  mod discussion? ban thread? AM link? 
    add that flair - ignore AM? up to debate to track users

[flair] /u/user (if not mod/AM) - title

check for artwork for unbans - sent by user, image link
'''

import time

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
  pass
