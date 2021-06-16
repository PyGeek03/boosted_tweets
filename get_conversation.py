import requests
import os
import json


from dotenv import load_dotenv
load_dotenv()


def create_tweet_url(ids, tweet_fields):    
    url = ("https://api.twitter.com/2/tweets?"
           f"ids={ids}&tweet.fields={tweet_fields}")
    return url


def create_headers():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    tweet_id = input("Tweet ID: ")
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs

    tweet_fields = "author_id,conversation_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_url = create_tweet_url(tweet_id, tweet_fields)
    headers = create_headers()
    json_response = connect_to_endpoint(tweet_url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
