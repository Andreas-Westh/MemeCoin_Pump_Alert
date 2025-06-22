import praw
import os
from dotenv import load_dotenv

# grab .env
load_dotenv()

# load in praw through .env
reddit = praw.Reddit(
    client_id    = os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET"),
    username     = os.getenv("USERNAME"),
    password     = os.getenv("PASSWORD"),
    user_agent   = os.getenv("USER_AGENT"),
    check_for_async=False
)

# check for success
print(reddit.user.me())