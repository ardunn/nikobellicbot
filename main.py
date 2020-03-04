import os
import time
import random
from collections import namedtuple
import praw
from praw.models import Comment
from praw.models import Submission

class Triggers:
    full = [
        "niko bellic",
        "bellic brothers",
        "nicobellicbot",
        "bellicbot",
        "hey cousin want to go bowling"
    ]

    partial = [
        "niko",
        "bellic",
        "grand theft auto",
        "grand theft auto iv",
        "grand theft auto 4",
        "gta",
        "gta iv",
        "gta 4",
    ]


def object_contains_trigger(obj, triggers):
    normal_body = obj.body.lower()
    if any([t in normal_body for t in triggers.full]) and obj.author.name != whoami:
        return True
    else:
        return False


def main_loop(reddit, replies, triggers):
    while 1:
        time.sleep(sleep_time)
        for subreddit in subreddits:
            for submission in reddit.subreddit(subreddit).new(limit=top_n_submissions):
                link = submission.permalink
                all_comments = submission.comments.list()
                for comment in all_comments:
                    if object_contains_trigger(comment, triggers):
                        comment.reply(random.choice(replies))

        # for submission in r.subreddit('gaming').hot(limit=2):
        #     print("--------------\n\n", submission.permalink)
        #     all_comments = submission.comments.list()
        #     print(len(all_comments))
        #     for obj in all_comments:
        #         print(obj.body)

        s = Submission(reddit, "fd5s31")
        for comment in s.comments.list():
            if comment_is_trigger(comment):
                comment.reply(random.choice(replies_md))


if __name__ == "__main__":
    whoami = "nikobellicbot2"
    sleep_time = 3600
    interval_time = 1
    subreddits = ("GTAIV", "gaming", "GrandTheftAutoV", "GrandTheftAuto", "GTA", "gtaonline", "rockstar")
    top_n_submissions = 5

    basedir = os.path.dirname(os.path.abspath(__file__))
    reply_logfile = os.path.join(basedir, "replies.log")
    voicedir = os.path.join(basedir, "voice")
    replies_mp3 = os.listdir(voicedir)
    n_replies = len(replies_mp3)
    gh_preface = "https://raw.githubusercontent.com/ardunn/nikobellicbot/master/voice/"
    replies_link = [gh_preface + mp3 for mp3 in replies_mp3]
    replies_txt = [s.replace(".mp3", "").replace("_", " ") for s in replies_mp3]
    replies_md = [f"[{replies_txt[i]}]({replies_link[i]})" for i in range(n_replies)]
    client_id = os.environ["NBB_REDDIT_CLIENT_ID"]
    client_secret = os.environ["NBB_REDDIT_CLIENT_SECRET"]
    username = os.environ["NBB_REDDIT_USERNAME"]
    password = os.environ["NBB_REDDIT_PASSWORD"]
    user_agent = os.environ["NBB_REDDIT_USER_AGENT"]
    triggers = Triggers()

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password
    )

    main_loop(reddit, replies_md, triggers)
