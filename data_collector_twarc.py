import os
import twarc
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client = twarc.Twarc2(bearer_token=bearer_token)  # only available if installed directly from tweepy's GitHub repo (aka development version)

count = 0
for response in client.search_recent(query="conversation_id:1404353357469212673",
                                     max_results=10):
    print(response["author"])
    count += 1
    if count == 2:
        break