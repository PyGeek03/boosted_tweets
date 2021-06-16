import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client = tweepy.Client(bearer_token)  # only available if installed directly from tweepy's GitHub repo (aka development version)

for tweet in tweepy.Paginator(client.search_recent_tweets, 
                              query="conversation_id:1404353357469212673",
                              expansions="author_id,referenced_tweets.id.author_id",
                              max_results=10).flatten(limit=50):
    print(tweet.author_id, tweet.referenced_tweets)