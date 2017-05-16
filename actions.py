import praw
import sqlite3

from datetime import date, timedelta
import calendar

from subreddits import subs_dict

reddit = praw.Reddit("modmail_bot")

def read_mod_actions(moderator, subreddit):
  exists = False
  actions = 0

  subreddit = subreddit.lower()

  db = sqlite3.connect("databases/mods.db")
  curs = db.cursor()

  curs.execute('''SELECT moderator, subreddit, actions FROM mods''')
  rows = curs.fetchall()
  
  for row in rows:
    if row[0] == moderator:
      if row[1] == subreddit:
        exists = True
        actions = row[2]
      else:
        pass

  db.close()
  return exists, actions

def add_mod_action(moderator, subreddit):
  db = sqlite3.connect("databases/mods.db")
  curs = db.cursor()

  subreddit = subreddit.lower()

  exists, actions = read_mod_actions(moderator, subreddit)

  if exists is False:
    curs.execute('''INSERT INTO mods(moderator, subreddit, actions) VALUES(?,?,?)''', (moderator, subreddit, 1))
  else:
    actions += 1
    curs.execute('''UPDATE mods SET actions = ? WHERE moderator = ? AND subreddit = ?''', (actions, moderator, subreddit))

  db.commit()
  db.close()

def post_mod_actions():
  db = sqlite3.connect("databases/mods.db")
  curs = db.cursor()

  curs.execute('''SELECT moderator, subreddit, actions FROM mods''')
  rows = curs.fetchall()

  postdate = date.today() - timedelta(days=7)
  month = calendar.month_name[postdate.month]
  year = postdate.year

  for key in subs_dict:
    mod_actions_title = "Moderator actions for " + month + " " + str(year) + " on /r/" + key
    mod_actions_body = "User: | Actions: | Percent: | \n :-- | --: | --: \n"
    mod_actions = {}
    total_actions = 0

    for row in rows:
      if str(key) == str(row[1]).lower():
        mod_actions.update({row[0]: row[2]})
        total_actions += row[2]
    
    sorted_mod_actions = sorted(mod_actions.items(), key=lambda x: x[1], reverse=True)

    for mod in sorted_mod_actions:
      percent = mod[1] / total_actions * 100
      percent = round(percent, 1)
      percent = str(percent) + "%"

      mod_actions_body += mod[0] + " | " + str(mod[1]) + " | " + percent + "\n"
    
    post = reddit.subreddit(subs_dict[key]).submit(mod_actions_title, selftext=mod_actions_body, send_replies=False)

    message_title = mod_actions_title
    message_body = mod_actions_title + " have been posted. Please [view here](" + post.permalink + "). \n\n*This is an automated message. Please do not reply.*"

    mods = reddit.subreddit(key).moderator()
    for mod in mods:
      if 'all' in mod.mod_permissions or 'mail' in mod.mod_permissions:
        reddit.redditor(mod.name).message(message_title, message_body, from_subreddit=key)


def reset_mod_actions():
  db = sqlite3.connect("databases/mods.db")
  curs = db.cursor()

  curs.execute('''DELETE FROM mods''')

  db.commit()
  db.close()

if __name__ == "__main__":
  post_mod_actions()
  reset_mod_actions()