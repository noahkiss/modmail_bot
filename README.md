## modmail_bot v2.0

*This is modmail_bot's first release. If you have issues, please open an issue. If you'd like to help contribute, feel free to open a pull request.*

## What is modmail_bot?

modmail_bot is designed to archive modmail threads from a specific subreddit to that subreddit's modmail backroom. This enables searching of modmail, which can be very useful to find previous user infractions, mod discussion topics, etc. Threads in the backroom will be updated with new replies, keeping an up-to-date reflection of the modmail threads.

In addition, modmail_bot will keep a running tally of moderator interactions in modmail, enabling subreddits to "fill in the gap" when it comes to mod stats. This is especially useful to judge new moderator engagement when deciding to promote/demote, because sometimes approvals/removals/bans don't tell the whole story, and modmail is a very important aspect to subreddit moderating. Each month a Mod Stats thread will be posted to the backroom sub to archive interactions, at which point the stats will be reset.

I hope to add more functionality in the future, and I am always open to suggestions! Some functionality that I hope to add in the future includes a slack plugin, the ability to query mod interaction stats on the fly, a comment chain nuke tool that doesn't require you to stay on the page (useful for large chains), etc.

## To run your own instance of modmail_bot, follow these steps:

1. Create the account you will use to run your instance of modmail_bot

2. Follow PRAW's [quick-start guide](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) to obtaining your reddit instance

3. [Clone or download](https://help.github.com/articles/cloning-a-repository/) this repository to your working directory

4. Rename praw.ini.example to praw.ini and fill in the 5 values. Leave the first line alone.

5. Run `pip3 install -r requirements.txt` to install dependencies. Note that `sqlite3 >= 3.16.0` is commented out - make sure your version is up to date. 

6. Run `python3 setup.py` and add in your `Main Subreddit/Modmail Subreddit` pairs. This will also initialize your database files.

7. Eventually `backfill.py` will catch you up on modmail. This has yet to be written.

8. The `modmail_bot.py` file is meant to run continuously. Do this however you like. Hint: you might start out with [screen](https://www.howtoforge.com/linux_screen), but I'm not really qualified to tell you how to keep it running.

9. Create a cron job to run `actions.py` on the first of every month, which will create a post in your modmail sub with moderator stats in modmail for the past month, and send out a mod mailer to everyone. Example cron job: `0 18 1 * * /usr/bin/python3 path/to/actions.py`

##### Make sure to check back for updates and added functionality in the future!

###### Feel free to reach out to me on reddit: [/u/noahjk](https://reddit.com/user/noahjk)