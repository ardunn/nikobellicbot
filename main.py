import random

import praw
from praw.models import Comment
from praw.models import Submission

from quotes import replies

r = praw.Reddit(

)

triggers = [
    "niko bellic",
    "bellic brothers",
    "nicobellicbot",
    "bellicbot",
    "hey cousin want to go bowling"
]

partial_triggers = [
    "niko",
    "bellic",
    "grand theft auto",
    "grand theft auto iv",
    "grand theft auto 4",
    "gta",
    "gta iv",
    "gta 4",
]


# print(r.read_only)

# for submission in r.subreddit('gaming').hot(limit=2):
#     print("--------------\n\n", submission.permalink)
#     all_comments = submission.comments.list()
#     print(len(all_comments))
#     for comment in all_comments:
#         print(comment.body)

whoami = "nikobellicbot2"


def comment_is_trigger(comment):
    normal_body = comment.body.lower()
    if any([t in normal_body for t in triggers]) and comment.author.name != whoami:
        return True
    else:
        return False



s = Submission(r, "fd5s31")
for comment in s.comments.list():
    if comment_is_trigger(comment):
        comment.reply(random.choice(replies))