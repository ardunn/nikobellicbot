import os
import time
import random
import itertools

import tqdm
import praw
from praw.exceptions import APIException


class Triggers:
    full = [
        "niko bellic",
        "bellic brothers",
        "nicobellicbot",
        "bellicbot",
        "hey cousin want to go bowling"
    ]

    gta_partials = [
        "grand theft auto",
        "grand theft auto iv",
        "grand theft auto 4",
        "liberty city",
        "gta",
        "gta iv",
        "gta 4",
    ]

    niko_partials = [
        "niko",
        "bellic",
    ]

    partials = list(itertools.product(gta_partials, niko_partials))


def object_contains_trigger(obj):
    normal_body = obj.body.lower()
    if any([t in normal_body for t in triggers.full]) or \
            any([all([p in normal_body for p in pset]) for pset in triggers.partials]):
        if gh_prefix not in normal_body:
            if obj.author.name != whoami:
                return True
    return False


def main_loop():
    while True:
        try:
            new_comments = 0
            for subreddit in subreddits:
                desc = f"In subreddit {subreddit}"
                for submission in tqdm.tqdm(reddit.subreddit(subreddit).hot(limit=top_n_submissions), desc=desc):

                    # Update comment tree to expand "more comments" sections
                    submission.comments.replace_more(limit=0)

                    # Add submission body to title for scanning for triggers
                    submission.body = str(submission.selftext) + " " + (submission.title)
                    all_objs = [submission] + submission.comments.list()

                    # Process all submission/comments together
                    for comment_or_submission in all_objs:
                        if object_contains_trigger(comment_or_submission):
                            permalink = str(comment_or_submission.permalink)
                            with open(reply_logfile, "r") as reply_log:
                                previous_permalinks = str(reply_log.read())
                            if permalink not in previous_permalinks:
                                time.sleep(interval_time)
                                reply = random.choice(replies)
                                comment_or_submission.reply(reply)
                                with open(reply_logfile, "a") as reply_log:
                                    reply_log.write(comment_or_submission.permalink + "\n")
                                new_comments += 1

                                if isinstance(comment_or_submission, praw.models.Comment):
                                    reply_type = "comment"
                                else:
                                    reply_type = "submission"

                                print(
                                    f"Replied {reply} on {reply_type} {permalink} on submission {submission.permalink}"
                                )
            print(f"\n---\n\tAdded {new_comments} comments.\n---\n")
            print(f"Sleeping {sleep_time} seconds...")
            time.sleep(sleep_time)
        except APIException:
            time.sleep(api_exception_time)


if __name__ == "__main__":
    whoami = "nikobellicbot"
    sleep_time = 60
    interval_time = 5
    api_exception_time = 120
    subreddits = ("GTAIV", "gaming", "GrandTheftAutoV", "GrandTheftAuto", "GTA", "gtaonline", "rockstar")
    # subreddits = ("testingground4bots",)
    top_n_submissions = 50

    basedir = os.path.dirname(os.path.abspath(__file__))

    reply_logfile = os.path.join(basedir, "replies.log")
    voicedir = os.path.join(basedir, "voice")
    replies_mp3 = os.listdir(voicedir)
    n_replies = len(replies_mp3)
    gh_prefix = "https://ardunn.github.io/nikobellicbot/voice/"
    replies_link = [gh_prefix + mp3 for mp3 in replies_mp3]

    long_clips = {
        "abbr_young_and_bitter": "Hah. War is where the young and stupid are tricked by the old and bitter into killing eachother. I was very young, and very angry. Maybe that is no excuse?",
        "abbr_traitor": "I know the traitor was not me. So for 10 years, I've been searching for the other two. One of them... lives here.",
        "abbr_cowering": "FIFTEEN minutes ago, you were cowering in fear because you didn't know what was going to happen. NOW, you know everything is shit, and we're going to be killed, and you're all cheerful? I don't get it!"
    }

    replies_txt = []
    for s in replies_mp3:
        s_no_ext = s.replace(".mp3", "").replace("{qmark}", "?")
        if s_no_ext in list(long_clips.keys()):
            replies_txt.append(long_clips[s_no_ext])
        else:
            replies_txt.append(s_no_ext.replace("_", " "))
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
