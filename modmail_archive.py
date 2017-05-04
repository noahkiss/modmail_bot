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
private moderator note to remind of unban image text format?
'''

import sqlite3
import praw

from secrets import client_id, client_secret, password, user_agent, username, modmail_db, mods_db, main_sub, modmail_sub, backroom_sub
try:
  from secrets import unban_sub
except ImportError:
  unban_sub = False

modmail_db   = sqlite3.connect(modmail_db)
mods_db      = sqlite3.connect(mods_db)

modmail_curs = modmail_db.cursor()
mods_curs    = mods_db.cursor()

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

def read_modmail():
  pass

def mailNew(id):
  pass

def mailOld(id):
  pass

def mailMod(id):
  pass

def threadPost(user, title, flair=None):
  pass

def threadUpdate(id):
  pass

def postArt(user, title, url):
  if unban_sub == False:
    pass
  else:
    pass

if __name__ == '__main__':
  pass
#modmailDB.commit()
#modmailDB.close()