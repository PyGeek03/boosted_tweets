import os
import json
import twarc
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client2 = twarc.Twarc2(bearer_token=bearer_token)

tweet_id = input("Input tweet ID: ")

data = []
for response in client2.tweet_lookup([tweet_id]):
    data.extend(response['data'])

query = f"conversation_id:{tweet_id}"
for response in client2.search_recent(query=query, max_results=100):
    data.extend(response["data"])

data.sort(key=lambda t: t["id"])

serialized_json = json.dumps(data,
                             indent=4,
                             sort_keys=True)
print(serialized_json)

filename = input("Filename to output to: ")
if filename == "":
    filename = "conversation_cache"
with open(f'outputs/{filename}.json', 'w') as f:
    f.writelines(serialized_json)