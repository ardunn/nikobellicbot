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

    # todo: not currently used
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


def object_contains_trigger(obj, triggers, reply_log):
    normal_body = obj.body.lower()
    permalink = obj.permalink
    if any([t in normal_body for t in triggers.full]):
        if permalink not in reply_log.readlines() and obj.author.name != whoami:
            return True
    return False


def main_loop():
    with open(reply_logfile, "a+") as reply_log:
        while True:
            new_comments = 0
            print(f"Sleeping {sleep_time} seconds...")
            time.sleep(sleep_time)
            for subreddit in subreddits:
                for submission in reddit.subreddit(subreddit).new(limit=top_n_submissions):
                    link = submission.permalink
                    all_comments = submission.comments.list()
                    for comment in all_comments:
                        if object_contains_trigger(comment, triggers, reply_log):
                            time.sleep(interval_time)
                            reply = random.choice(replies)
                            comment.reply(reply)
                            reply_log.write(comment.permalink + "\n")
                            new_comments += 1
                            print(f"Replied {reply} on comment {comment.permalink} on submission {submission.permalink}")
            print(f"\n---\n\tAdded {new_comments} comments.\n---\n")

if __name__ == "__main__":
    whoami = "nikobellicbot2"
    sleep_time = 2
    interval_time = 1
    # subreddits = ("GTAIV", "gaming", "GrandTheftAutoV", "GrandTheftAuto", "GTA", "gtaonline", "rockstar")
    subreddits = ("testingground4bots",)
    top_n_submissions = 3

    basedir = os.path.dirname(os.path.abspath(__file__))

    reply_logfile = os.path.join(basedir, "replies.log")
    voicedir = os.path.join(basedir, "voice")
    replies_mp3 = os.listdir(voicedir)
    n_replies = len(replies_mp3)
    gh_preface = "https://raw.githubusercontent.com/ardunn/nikobellicbot/master/voice/"
    replies_link = [gh_preface + mp3 for mp3 in replies_mp3]
    replies_txt = [s.replace(".mp3", "").replace("_", " ") for s in replies_mp3]
    replies = [f"[{replies_txt[i]}]({replies_link[i]})" for i in range(n_replies)]

    triggers = Triggers()

    client_id = os.environ["NBB_REDDIT_CLIENT_ID"]
    client_secret = os.environ["NBB_REDDIT_CLIENT_SECRET"]
    username = os.environ["NBB_REDDIT_USERNAME"]
    password = os.environ["NBB_REDDIT_PASSWORD"]
    user_agent = os.environ["NBB_REDDIT_USER_AGENT"]

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
        username=username,
        password=password
    )

    main_loop()
