import os
import random

import praw
from praw.models import Comment
from praw.models import Submission


def comment_is_trigger(comment):
    normal_body = comment.body.lower()
    # if any([t in normal_body for t in TRIGGERS]) and comment.author.name != whoami:
    if any([t in normal_body for t in TRIGGERS]):
        return True
    else:
        return False


def main_loop():
    while 1:

        # for submission in r.subreddit('gaming').hot(limit=2):
        #     print("--------------\n\n", submission.permalink)
        #     all_comments = submission.comments.list()
        #     print(len(all_comments))
        #     for comment in all_comments:
        #         print(comment.body)

        s = Submission(reddit, "fd5s31")
        for comment in s.comments.list():
            if comment_is_trigger(comment):
                comment.reply(random.choice(replies_md))


if __name__ == "__main__":
    whoami = "nikobellicbot2"
    voicedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice")
    replies_mp3 = os.listdir(voicedir)
    n_replies = len(replies_mp3)
    gh_preface = "https://raw.githubusercontent.com/ardunn/nikobellicbot/master/voice/"
    replies_link = [gh_preface + mp3 for mp3 in replies_mp3]
    replies_txt = [s.replace(".mp3", "").replace("_", " ") for s in replies_mp3]
    replies_md = [f"[{replies_txt[i]}]({replies_link[i]})" for i in range(n_replies)]

    TRIGGERS = [
        "niko bellic",
        "bellic brothers",
        "nicobellicbot",
        "bellicbot",
        "hey cousin want to go bowling"
    ]

    TRIGGERS_PARTIAL = [
        "niko",
        "bellic",
        "grand theft auto",
        "grand theft auto iv",
        "grand theft auto 4",
        "gta",
        "gta iv",
        "gta 4",
    ]

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
