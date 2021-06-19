import json
import treelib
import treelib.exceptions
import argparse

def tag_acc_if_bot(acc, threshold, checked_accounts):
    if acc not in checked_accounts:
        return f"User ID: {acc}"
    elif "error" in checked_accounts[acc]:
        return f"User ID: {acc} (Botometer check failed)"
    botometer_output = checked_accounts[acc]
    username = botometer_output["user"]["user_data"]["screen_name"]
    majority_lang = botometer_output["user"]["majority_lang"]
    cap_scores = botometer_output["cap"]
    score = cap_scores["english"] if majority_lang == "en" \
            else cap_scores["universal"]
    probability = int(score * 100)
    if probability > threshold:
        return f'{username} (bot: {probability}% probability)'
    return username
        

def visualize_api2(tweets, threshold, checked_accounts):
    tweets.sort(key=lambda t: t['id'])
    tree = treelib.Tree()

    root_tweet = tweets[0]
    rootID = root_tweet["id"]
    root_acc = tag_acc_if_bot(root_tweet["author_id"], threshold, checked_accounts)
    tree.create_node(tag=root_acc, identifier=rootID)

    for i, tweet in enumerate(tweets[1:]):
        tweetID = tweet["id"]
        tweet_acc = tag_acc_if_bot(tweet["author_id"], threshold, checked_accounts)
        parentID = tweet["referenced_tweets"][0]["id"]
        try:
            tree.create_node(tag=tweet_acc,
                             identifier=tweetID,
                             parent=parentID)
        except treelib.exceptions.NodeIDAbsentError:
            tree.create_node(tag="(Deleted tweet)",
                             identifier=parentID,
                             parent=rootID)
            tree.create_node(tag=tweet_acc,
                             identifier=tweetID,
                             parent=parentID)

    return str(tree)


def visualize_conversation(conversation_json_file, threshold):
    with open(conversation_json_file, 'r') as f:
        data = json.load(f)
    tweets = data["data"]

    botometer_output_file = "outputs/botometer_cache.json"
    with open(botometer_output_file, 'r') as f:
        checked_accounts = json.load(f)

    tree = visualize_api2(tweets, threshold, checked_accounts)
    print(tree)

    users = set(tweet["author_id"] for tweet in tweets)  # Twitter API v2
    #users = set(tweet["user"]["id"] for tweet in tweets)  # Twitter API v1
    print(f'Number of accounts: {len(users)}')
    print(f'Number of tweets: {len(tweets)}')

    conversation_filename = conversation_json_file[:-5]
    conversation_tree_file = f"{conversation_filename}-tree.txt"
    with open(conversation_tree_file, 'w') as f:
        f.writelines(tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=("Visualise the tree of the conversation, "
                     "whose root is the original tweet's author " 
                     "and other nodes are the retweeters and authors of replies")
    )
    parser.add_argument('conversation_files', metavar='[FILE]', type=str, nargs='+',
                        help=("one or more json files, each file consisting of"
                              "the whole conversation associated with a Tweet")
    )

    parser.add_argument('--threshold', dest='threshold', type=int, default=80,
                        help='custom threshold percentage for bot probability (default: 80)')

    args = parser.parse_args()
    for filename in args.conversation_files:
        visualize_conversation(filename, args.threshold)