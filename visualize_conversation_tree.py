import json
from treelib import Tree


def visualize_api2(tweets):
    tree = Tree()

    # after sorting by id, first tweet would be the root
    tweets.sort(key=lambda t: t["id"])
    root_tweet = tweets[0]
    rootID = root_tweet["referenced_tweets"][0]["id"]
    tree.create_node(rootID, identifier=rootID, data="root")

    for i, tweet in enumerate(tweets[1:]):
        print(i)
        tweetID = tweet["id"]
        parentID = tweet["referenced_tweets"][0]["id"]
        tree.create_node(tweetID,
                         identifier=tweetID,
                         data=tweet,
                         parent=parentID)

    tree.show()

#json_file = "elon_tweet.json"
json_file = "lex_tweet-twarc1.json"
with open(json_file, 'r') as f:
    data = json.load(f)
tweets = data["data"]
#users = set(tweet["author_id"] for tweet in tweets)  # Twitter API v2
users = set(tweet["user"]["id"] for tweet in tweets)  # Twitter API v1
#print(len(users))
#print(len(tweets))
visualize_api2(tweets)