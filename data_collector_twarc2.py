import os
import json
import twarc
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client = twarc.Twarc2(bearer_token=bearer_token)

count = 0
data = []
tweet_id = 1404353357469212673
query = f"conversation_id:{tweet_id}"
for response in client.search_recent(query=query, max_results=10):
    data.extend(response["data"])
    count += 1
    if count == 2:
        break

serialized_json = json.dumps(data,
                             indent=4,
                             sort_keys=True)
print(serialized_json)
filename = input("Filename to output to: ")
with open(f'{filename}.json', 'w') as f:
    f.writelines(serialized_json)