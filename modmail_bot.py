#!/usr/bin/python3

import praw
import sqlite3

from subreddits import subs_dict

import actions

reddit = praw.Reddit("modmail_bot")

# temporary - due to bug in getting all modmail messages from reddit API #
state_switch = ""
state_vers = 1

class Modmail_bot():
  
  def read_modmail(self):
    
    # temporary #
    global state_switch, state_vers
    if state_vers == 1:
      state_switch = "all"
    elif state_vers == 2:
      state_switch = "archived"
    elif state_vers == 3:
      state_switch = "mod"
    # temporary #

    for mail in reddit.subreddit("all").modmail.conversations(limit=30, state=state_switch): # state_switch part of temporary #
      post_body = "####https://mod.reddit.com/mail/all/" + mail.id + "\n\n---\n\n"
      title = ""

      try:
        sub_main = str(mail.owner).lower()
        sub_mail = subs_dict[sub_main]
      except KeyError:
        print("/r/" + sub_main + " has no mail subreddit, skipping message")
        continue

      mail_exists, num_replies = self.db_read(mail.id)

      if mail_exists is not False and mail.num_messages == num_replies:
        continue
      
      moderators = []
      mods = reddit.subreddit(sub_main).moderator()
      for mod in mods:
        moderators.append(mod.name)

      # hopefully temporary #
      try:
        title += str(mail.user)
      except:
        title += "Mod thread"
      # hopefully temporary #

      title += " | " + mail.subject + " (" + mail.messages[0].date[:10] + ")"
      count = 1

      for message in mail.messages:
        post_body += "####[/u/" + message.author.name

        if message.is_internal:
          post_body += " (private)](##private)"
          if count > num_replies:
            actions.add_mod_action(str(message.author.name), str(mail.owner))
        elif message.author.name in moderators:
          post_body += "](##mod)"
          if count > num_replies:
            actions.add_mod_action(str(message.author.name), str(mail.owner))
        else:
          post_body += " (user)](https://reddit.com/user/" + message.author.name + "#op)"

        if len(message.body_markdown) > 500:
          message_body = message.body_markdown[:500] + "..."
        else:
          message_body = message.body_markdown
        post_body +=  "\n\n" + message_body + "\n\n---\n\n"

        count += 1

      if mail_exists is not False:
        self.post_thread(mail, post_body, title, sub_mail)
      else:
        self.post_thread(mail, post_body, title, sub_mail, new=True)

    # temporary #
    if state_switch == "all":
      state_vers = 2
    elif state_switch == "archived":
      state_vers = 3
    elif state_switch == "mod":
      state_vers = 1
    # temporary #

  def read_messages(self):
    #actions.read_mod_actions
    pass

  def post_thread(self, mail, body, title, sub_mail, new=False):
    if new is True:
      post = reddit.subreddit(sub_mail).submit(title, selftext=body, send_replies=False)
      self.db_write(mail.id, mail.num_messages, thread_id=post.id)
      print("Created: " + title + " | subreddit: " + sub_mail)
    else:
      thread_id, unused = self.db_read(mail.id)
      self.db_write(mail.id, mail.num_messages)
      submission = reddit.submission(id=thread_id)
      try:
        submission.edit(body)
        print("Updated: " + title + " | subreddit: " + sub_mail)
      except:
        post = reddit.subreddit(sub_mail).submit(title, selftext=body, send_replies=False)
        submission.delete()
        self.db_write(mail.id, mail.num_messages, thread_id=post.id)
        print("Reposted: " + title + " | subreddit: " + sub_mail)

  def db_read(self, id):
    exists = False
    replies = 0
    db = sqlite3.connect("databases/posts.db")
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

  def db_write(self, modmail_id, replies, thread_id=None):
    db = sqlite3.connect("databases/posts.db")
    curs = db.cursor()
    exists, unused = self.db_read(modmail_id)

    if exists == False:
      curs.execute('''INSERT INTO modmail(modmail_id, backroom_id, replies) VALUES(?,?,?)''', (modmail_id, thread_id, replies))
    else:
      if thread_id == None:
        curs.execute('''UPDATE modmail SET replies = ? WHERE modmail_id = ?''', (replies, modmail_id))
      else:
        curs.execute('''UPDATE modmail SET backroom_id = ?, replies = ? WHERE modmail_id = ?''', (thread_id, replies, modmail_id))

    db.commit()
    db.close()

if __name__ == "__main__":
  bot = Modmail_bot()
  while True:
    bot.read_modmail()