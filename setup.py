# database initialization
# subreddit key pair initialization subreddits.py lower()
import sqlite3
import os.path

if __name__ == '__main__':

  # create database files
  posts = 'databases/posts.db'
  mods = 'databases/mods.db'

  try:
    os.mkdir('databases')
  except:
    pass

  try:
    open(posts, 'x')
  except FileExistsError:
    pass

  db = sqlite3.connect("databases/posts.db")
  curs = db.cursor()

  curs.execute('''CREATE TABLE modmail (modmail_id TEXT PRIMARY KEY, backroom_id TEXT, replies INTEGER)''')

  db.commit()
  db.close()

  try:
    open(mods, 'x')
  except FileExistsError:
    pass

  db = sqlite3.connect("databases/mods.db")
  curs = db.cursor()

  curs.execute('''CREATE TABLE mods (moderator TEXT PRIMARY KEY, subreddit TEXT, actions INTEGER)''')

  db.commit()
  db.close()

  # create subreddits.py

  subreddits = {}
  while True:
    main_sub = input("Enter main subreddit here (press enter if done):").lower()
    if main_sub is "":
      break
    mail_sub = input("Enter cooresponding modmail subreddit here:").lower()
    subreddits.update({main_sub: mail_sub})

  with open('subreddits.py', 'w') as file:
    file.write("subs_dict = " + str(subreddits))