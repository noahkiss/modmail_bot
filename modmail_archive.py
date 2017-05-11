#!/usr/bin/python3
#praw 4.5.1

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

moderators = []
mods = sub_main.moderator()
for mod in mods:
  moderators.append(mod.name)

#temporary
state_switch = ""
iteration = 1

def read_modmail():
  #temporary
  global state_switch, iteration
  if iteration == 1:
    state_switch = "all"
    print("Using state_switch 1 - all")
  elif iteration == 2:
    state_switch = "archived"
    print("Using state_switch 2 - archived")
  elif iteration == 3:
    state_switch = "mod"
    print("Using state_switch 3 - mod")

  for mail in sub_main.modmail.conversations(limit=15, state=state_switch):

    post_body = "https://mod.reddit.com/mail/all/" + mail.id + "\n\n---\n\n"

    title = ""
    try:
      title += str(mail.user)
    except:
      title += "Mod thread"
    title += " | " + mail.subject + " (" + mail.messages[0].date[:10] + ")"
    for message in mail.messages:
      post_body += "####[/u/" + message.author.name
      if message.is_internal:
        post_body += " (private)](##private)"
      elif message.author.name in moderators:
        post_body += "](##mod)"
      else:
        post_body += " (user)](##op)"
      if len(message.body_markdown) > 500:
        message_body = message.body_markdown[:500] + "..."
      else:
        message_body = message.body_markdown
      post_body +=  "\n\n" + message_body + "\n\n---\n\n"

    mail_exists, num_replies = db_read(id=mail.id)

    if mail_exists != False:
      if mail.num_messages > num_replies:
        mail_old(mail, post_body, title)

        #TODO count all new mails, add mod action for mod
    else:
      mail_new(mail, post_body, title)

  #temporary
  if state_switch == "all":
    iteration = 2
    print("Switching to iteration 2 - archived")
  elif state_switch =="archived":
    iteration = 3
    print("Switching to iteration 3 - mod")
  elif state_switch == "mod":
    iteration = 1
    print("Switching to iteration 1 - all")

def mail_new(mail, body, title):
  post = sub_modmail.submit(title, selftext=body, send_replies=False)
  db_write(mail.id, mail.num_messages, thread_id=post.id)
  print("Created: " + title + " | replies: " + str(mail.num_messages))

def mail_old(mail, body, title):
  thread_id, asdf = db_read(mail.id)
  db_write(mail.id, mail.num_messages)
  submission = r.submission(id=thread_id)

  try:
    submission.edit(body)
    print("Updated: " + title + " | replies: " + str(mail.num_messages))
  except:
    post = sub_modmail.submit(title, selftext=body, send_replies=False)
    submission.delete()
    db_write(mail.id, mail.num_messages, thread_id=post.id)
    print("Reposted: " + title + " | replies: " + str(mail.num_messages))

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