#modmail_bot v2.0
---

**This is modmail_bot's first release. If you have issues, please open an issue. If you'd like to help contribute, feel free to open a pull request.**
---

##To run your own instance of modmail_bot, follow these steps:

1. Create the account you will use to run your instance of modmail_bot

2. Follow PRAW's [quick-start guide](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) to obtaining your reddit instance

3. Rename praw.ini.example to praw.ini and fill in the 5 values. Leave the first line alone.

4. Run `pip install -r requirements.txt` to install dependencies. 

5. Run `python3 setup.py` and add in your `Main Subreddit/Modmail Subreddit` pairs. This will also initialize your database files.

6. Eventually `backfill.py` will catch you up on modmail. This has yet to be written.

7. The `modmail_bot.py` file is meant to run continuously. Do this however you like. Hint: you might start out with [screen](https://www.howtoforge.com/linux_screen), but I'm not really qualified to tell you how to keep it running.

8. Create a cron job to run `actions.py` on the first of every month, which will create a post in your modmail sub with moderator stats in modmail for the past month, and send out a mod mailer to everyone. Example cron job: `0 18 1 * * /usr/bin/python3 path/to/actions.py`
---

#####Make sure to check back for updates and added functionality in the future!

######Feel free to reach out to me on reddit: [/u/noahjk](https://reddit.com/user/noahjk)