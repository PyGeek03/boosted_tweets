import json
from treelib import Tree


def visualize(tweets):
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


with open("elon_tweet.json", 'r') as f:
    data = json.load(f)
tweets = data["data"]
users = set(tweet["author_id"] for tweet in tweets)
print(len(users))
print(len(tweets))
#visualize(tweets)