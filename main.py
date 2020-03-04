import os
import time
import random
import tqdm
import praw


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

    anti = [
        "/ardunn/nikobellicbot"
    ]


def object_contains_trigger(obj):
    normal_body = obj.body.lower()
    if any([t in normal_body for t in triggers.full]):
        if not any([t in normal_body for t in triggers.anti]):
            if obj.author.name != whoami:
                return True
    return False


def main_loop():
    while True:
        new_comments = 0
        for subreddit in subreddits:
            desc = f"In subreddit {subreddit}"
            for submission in tqdm.tqdm(reddit.subreddit(subreddit).hot(limit=top_n_submissions), desc=desc):
                submission_permalink = submission.permalink
                all_comments = submission.comments.replace_more(limit=0)
                all_comments = [c for c in all_comments if isinstance(praw.models.Comment)]
                for comment in all_comments:
                    if object_contains_trigger(comment):
                        comment_permalink = str(comment.permalink)
                        with open(reply_logfile, "r") as reply_log:
                            previous_permalinks = str(reply_log.read())
                        if comment_permalink not in previous_permalinks:
                            time.sleep(interval_time)
                            reply = random.choice(replies)
                            comment.reply(reply)
                            with open(reply_logfile, "a") as reply_log:
                                reply_log.write(comment.permalink + "\n")
                            new_comments += 1
                            print(
                                f"Replied {reply} on comment {comment_permalink} on submission {submission_permalink}"
                            )
        print(f"\n---\n\tAdded {new_comments} comments.\n---\n")
        print(f"Sleeping {sleep_time} seconds...")
        time.sleep(sleep_time)


if __name__ == "__main__":
    whoami = "nikobellicbot2"
    sleep_time = 60
    interval_time = 5
    subreddits = ("GTAIV", "gaming", "GrandTheftAutoV", "GrandTheftAuto", "GTA", "gtaonline", "rockstar", "testingground4bots")
    # subreddits = ("testingground4bots",)
    top_n_submissions = 100

    basedir = os.path.dirname(os.path.abspath(__file__))

    reply_logfile = os.path.join(basedir, "replies.log")
    voicedir = os.path.join(basedir, "voice")
    replies_mp3 = os.listdir(voicedir)
    n_replies = len(replies_mp3)
    gh_preface = "https://ardunn.github.io/nikobellicbot/voice/"
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
