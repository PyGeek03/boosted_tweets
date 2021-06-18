# boosted_tweets_dataset
A set of scripts being developed with the goal to collect a dataset of viral tweets that exhibit signs of being automatically propagated.

Workflow:
- Find viral tweets, possibly by finding trending topics
- Get the whole conversations associated to such viral tweets
- Use Botometer API to check if participating accounts in these conversations are bots
- Visualize the conversation, as a tree whose root is the original tweet's author and other nodes are the retweeters and authors of replies. Accounts that might be bot will be tagged with bot probability score. The children nodes of the same parent node are ordered according to their tweet's timestamp.