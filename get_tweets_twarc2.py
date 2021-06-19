import os
import json
import twarc
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client2 = twarc.Twarc2(bearer_token=bearer_token)

tweets_input = input("Input tweet IDs, seperated by space: ")
tweet_ids = tweets_input.split()

data = []
for response in client2.user_lookup(tweet_ids):
    data.extend(response['data'])

serialized_json = json.dumps(data,
                             indent=4,
                             sort_keys=True)
print(serialized_json)

filename = input("Filename to output to: ")
if filename == "":
    filename = "tweets_cache"
with open(f'outputs/{filename}.json', 'w') as f:
    f.writelines(serialized_json)