import os
import twarc
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")
client = twarc.Twarc2(bearer_token=bearer_token)

count = 0
data = []
query = "conversation_id:1404353357469212673"
for response in client.search_recent(query=query, max_results=10):
    data.extend(response["data"])
    count += 1
    if count == 2:
        break
[print(row) for row in data]
