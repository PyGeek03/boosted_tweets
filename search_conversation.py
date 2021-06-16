import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def create_search_url(query: dict, tweet_fields: list):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    query_string = "".join(str(k) + ":" + str(v) for k, v in query.items())
    tweet_fields_string = "".join(tweet_fields)
    url = ("https://api.twitter.com/2/tweets/search/recent?"
           f"query={query_string}&tweet_fields={tweet_fields_string}")

    return url


def create_headers():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    query = {"conversation_id": conversation_id}
    tweet_fields = ["author_id", "created_at", "in_reply_to_user_id"]
    url = create_search_url(query, tweet_fields)
    headers = create_headers()
    json_response = connect_to_endpoint(url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
