import time
import requests
import os
import json

from treelib import Tree
from dotenv import load_dotenv
load_dotenv()

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    if response.text == 'Rate limit exceeded\n':
        reset_time = int(response.headers["x-rate-limit-reset"])
        sleep_time = max(0, reset_time - int(time.time()) + 1)
        print(f'Sleep for {sleep_time} seconds')
        time.sleep(sleep_time)
        response = requests.request("GET", url, headers=headers)
        print('OK!')
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweet_json(ids, tweet_fields, headers):
    url = ("https://api.twitter.com/2/tweets?"
           f"ids={ids}&tweet.fields={''.join(tweet_fields)}")
    json_response = connect_to_endpoint(url, headers)
    return json_response


def get_search_json(query, tweet_fields, headers):
    query_string = "".join(str(k) + ":" + str(v) for k, v in query.items())
    tweet_fields_string = ",".join(tweet_fields)
    max_results = 100
    main_url = ("https://api.twitter.com/2/tweets/search/recent?"
                f"query={query_string}"
                f"&tweet.fields={tweet_fields_string}"
                f"&max_results={max_results}")
    json_response = connect_to_endpoint(main_url, headers)
    data = json_response["data"]

    while "next_token" in json_response["meta"]:
        next_token = json_response["meta"]["next_token"]
        url = main_url + f"&next_token={next_token}"
        json_response = connect_to_endpoint(url, headers)
        data.extend(json_response["data"])

    return {"data": data}


def create_headers():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def visualize(tweets):
    tree = Tree()

    # after sorting by timestamps, first tweet would be the root
    tweets.sort(key=lambda t: t["created_at"])
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


def main():
    headers = create_headers()

    tweet_id = input("Tweet ID: ")
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    tweet_fields = ["conversation_id"]
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_json_response = get_tweet_json(tweet_id, tweet_fields, headers)
    print(tweet_json_response)

    conversation_id = tweet_json_response["data"][0]["conversation_id"]

    query = {"conversation_id": conversation_id}
    tweet_fields = ["author_id", "created_at", "in_reply_to_user_id",
                    "referenced_tweets"]
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    search_json_response = get_search_json(query, tweet_fields, headers)

    serialized_json = json.dumps(search_json_response,
                                 indent=4,
                                 sort_keys=True)
    print(serialized_json)
    filename = input("Filename to write to: ")
    with open(f'{filename}.json', 'w') as f:
        f.writelines(serialized_json)

    # print(serialized_json)
    tweets = search_json_response["data"]
    visualize(tweets)


if __name__ == "__main__":
    main()
