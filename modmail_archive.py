#!/usr/bin/python3
#praw 4.5.1

from time import sleep

import sqlite3
import praw

from secrets import client_id, client_secret, password, user_agent, username, modmail_db, mods_db, main_sub, modmail_sub

r = praw.Reddit(client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=username,
                password=password)

sub_main     = r.subreddit(main_sub)
sub_modmail  = r.subreddit(modmail_sub)

def read_modmail():
  for mail in sub_main.modmail.conversations():
    
    post_body = ""

    title = mail.authors[0].name + " | " + mail.subject + " (" + mail.messages[0].date[:10] + ")"

    for message in mail.messages:
      post_body += "####[/u/" + message.author.name
      if message.is_internal:
        post_body += " (private)](/#private)"
      elif mail.authors[0].name == message.author.name:
        post_body += " (user)](/#op)"
      else:
        post_body += "](/#mod)"
      post_body +=  "\n\n" + message.body_markdown + "\n\n---\n\n"

    mail_exists, num_replies = db_read(id=mail.id)

    if mail_exists != False:
      if mail.num_messages > num_replies:
        mail_old(mail, post_body)

        #TODO count all new mails, add mod action for mod
    else:
      mail_new(mail, post_body, title)

      #if mail.is_internal: figure out how to read mod discussions tbd
      # if mail.subject == "You've been banned from participating in r/" + mail.owner.display_name:
      #   title += " [Ban thread]" just do this with automod?
      # add mod actions for mods

def mail_new(mail, body, title):
  post = sub_modmail.submit(title, selftext=body, send_replies=False)
  print(title + " || " + str(mail.num_messages))
  db_write(mail.id, mail.num_messages, thread_id=post.id)

def mail_old(mail, body):
  thread_id = db_read(mail.id)
  db_write(mail.id, mail.num_replies)
  submission = sub_modmail.Submission(r, id=thread_id)

  try:
    submission.edit(body)
  except:
    post = sub_modmail.submit(submission.title, selftext=body, send_replies=False)
    submission.delete()
    db_write(mail.id, mail.num_messages, thread_id=post.id)

def db_read(id):
  exists = False
  replies = 0
  db = sqlite3.connect(modmail_db)
  curs = db.cursor()

  curs.execute('''SELECT modmail_id, backroom_id, replies FROM modmail''')
  rows = curs.fetchall()
  
  for row in rows:
    if row[0] == id:
      exists = row[1]
      replies = row[2]
      break

  db.close()
  return exists, replies

def db_write(modmail_id, replies, thread_id=None):
  db = sqlite3.connect(modmail_db)
  curs = db.cursor()
  exists, asdf = db_read(modmail_id)

  if exists == False:
    curs.execute('''INSERT INTO modmail(modmail_id, backroom_id, replies) VALUES(?,?,?)''', (modmail_id, thread_id, replies))
  else:
    if thread_id == None:
      curs.execute('''UPDATE modmail SET replies = ? WHERE modmail_id = ?''', (replies, modmail_id))
    else:
      curs.execute('''UPDATE modmail SET backroom_id = ?, replies = ? WHERE modmail_id = ?''', (thread_id, replies, modmail_id))

  db.commit()
  db.close()

def db_mod_actions(user):
  db = sqlite3.connect(mods_db)
  curs = db.cursor()

  db.commit()
  db.close()

if __name__ == '__main__':
  while True:
    read_modmail()
    sleep(30)