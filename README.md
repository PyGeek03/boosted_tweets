# boosted_tweets
A set of scripts being developed with the goal to collect a dataset of viral tweets that exhibit signs of being automatically propagated.

## Quickstart:
1. Clone this repo and change your working directory to it
2. Install all dependencies:
```
$ pip install -r requirements.txt
```
3. Sign up for access to [Twitter API](https://developer.twitter.com/en/apply/user.html) and [Botometer API](https://rapidapi.com/OSoMe/api/botometer-pro)
4. Create a new file called `.env`, whose content is the API keys:
```
CONSUMER_KEY={Twitter API's consumer key}
CONSUMER_SECRET={Twitter API's consumer secret key}
ACCESS_TOKEN={Twitter API's access token}
ACCESS_TOKEN_SECRET={Twitter API's access token secret key}
BEARER_TOKEN={Twitter API's bearer token}

RAPIDAPI_KEY={Rapid API key, to access Botometer API}
```

## Workflow:
1. Find a viral tweets, possibly by finding trending topics (using `get_trends_twarc1.py`) and then searching for related tweets (using `get_top_trending_tweets_twarc1.py`)
2. Get the whole conversation (retweets and replies) associated with this tweet (using `get_conversation_twarc2.py`). This conversation will be saved to a JSON file
3. Use Botometer API to check if participating accounts in this conversation are bots (using `use_botometer.py` and the above JSON file)
4. Visualize the conversation (using `visualize_conversation_tree.py` and the above JSON file), as a tree whose root is the author of the original tweet and other nodes are the authors of retweets and replies. Accounts that might be bot will be tagged with bot probability score. Sibling nodes (children of the same parent node) are ordered according to their tweet's timestamp.

## Dependencies:
- botometer==1.6
- python-dotenv==0.17.1
- requests==2.25.1
- treelib==1.6.1
- twarc==2.1.7
- tweepy==3.10.0