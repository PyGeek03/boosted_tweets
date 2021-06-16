import json
from treelib import Tree

# Load the data
with open("tweets.json", 'r') as f:
    data = json.load(f)

#  Get just the tweets
tweets = data["data"]

#  Sort the tweets
tweets.sort(key=lambda t: t["created_at"])

#  Tree Structure
tree = Tree()

#  First Parent is the root
rootID = tweets[0]["referenced_tweets"][0]["id"]
tree.create_node(rootID, identifier=rootID, data="root")

#  Load the Tweets into a Tree Structure
for i, tweet in enumerate(tweets):
    print(i)
    tweetID = tweet["id"]
    parentID = tweet["referenced_tweets"][0]["id"]
    tree.create_node(tweetID, identifier=tweetID, data=tweet, parent=parentID)

#  Display the Tree
tree.show()