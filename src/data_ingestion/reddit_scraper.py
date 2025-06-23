import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.loaders import tickers
from src.utils.config import SUBREDDITS
import praw
from dotenv import load_dotenv
import nltk
import pandas as pd
from sentida import Sentida



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

# Subreddits we want to scrape
subreddit = reddit.subreddit("+".join(SUBREDDITS))
    # may have to make into a loop to store subreddit name

# sorting the posts / how many amounts to scrape
submissions = list(subreddit.hot(limit=1000)) # must be a list so we can iterate through it multiple times
for submission in submissions:
    print(f"submission.title: {submission.title}")


# tokenize the words in the title
word_collection=[]
for submission in submissions:
    title_words = nltk.word_tokenize(submission.title,language="english")
    word_collection.extend(title_words)

# tickers to lower too
tickers_lower = [t.lower() for t in tickers]

# match if a word is one of our tickers
potential_tickers = [
    word for word in word_collection
    if word in tickers or word in tickers_lower
]


# get titles that include the ticker
ticker_titles_rows = []

for submission in submissions:
    for ticker in potential_tickers:
        if ticker in submission.title:
            ticker_titles_rows.append({
                    "ticker": ticker,
                    "title": submission.title
                 })
           # break # doesnt match same submission more than once, could be removed

# create a df for above loop hell
ticker_titles = pd.DataFrame(ticker_titles_rows, columns=["ticker","title"])

# get sentiment
ticker_titles["sentiment"] = ticker_titles["title"].apply(lambda x: Sentida().sentida(x,output="mean",normal=False))
