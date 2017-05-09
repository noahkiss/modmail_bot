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
private mod note for suicide thingy?
'''

from time import sleep

import sqlite3
import praw

from secrets import client_id, client_secret, password, user_agent, username, modmail_db, mods_db, main_sub, modmail_sub, backroom_sub
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

def read_modmail():
  for mail in sub_main.modmail.conversations():
    
    post_body = ""

    title = mail.authors[0].name + " | " + mail.subject + " (" + mail.messages[0].date[:10] + ")"

    for message in mail.messages:
      post_body += "####/u/" + message.author.name + ":"
      if message.is_internal:
        post_body += " (Private)"
      if mail.authors[0].name == message.author.name:
        post_body += " (OP)"
      post_body +=  "\n\n" + message.body_markdown + "\n\n---\n\n"

    mail_exists, num_replies = db_read(id=mail.id)

    if mail_exists:
      if mail.num_messages > num_replies:
        mail_old(mail.id, post_body)
        #count all new mails, add mod action for mod
    else:
      #if mail.is_internal: figure out how to read mod discussions tbd
      # if mail.subject == "You've been banned from participating in r/" + mail.owner.display_name:
      #   title += " [Ban thread]" just do this with automod?
      mail_new(mail.id, post_body, title)
      #add mod actions for mods

def mail_new(id, body, title):
  print(title)
  #write db for new mail here after submitting

def mail_old(id, body):
  print(id)

# def post_art(user, title, image_url):
#   if unban_sub != False:
#     post_title = title + " by /u/" + user
#     sub_unban.submit(post_title, url=image_url, send_replies=False)
#   else:
#     pass

def db_read(id):
  exists = False
  db = sqlite3.connect(modmail_db)
  curs = db.cursor()

  #exists = True
  #read post id, if it exists return true and actions, if not return false and zero

  db.commit()
  db.close()
  return exists, 2

def db_write(id):
  db = sqlite3.connect(modmail_db)
  curs = db.cursor()

  db.commit()
  db.close()

def db_mod_numbers(user):
  db = sqlite3.connect(mods_db)
  curs = db.cursor()

  db.commit()
  db.close()

if __name__ == '__main__':
  while True:
    read_modmail()
    sleep(30)