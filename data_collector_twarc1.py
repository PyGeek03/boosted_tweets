import os
import twarc
import json
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
client = twarc.Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

tweet_ids = ['1404353357469212673', '1404353618518499329']
retweets = {'data': list(client.retweets(tweet_ids))}
serialized_json = json.dumps(retweets,
                             indent=4,
                             sort_keys=True)
print(serialized_json)
with open('twarc1_output.json', 'w') as f:
    f.writelines(serialized_json)