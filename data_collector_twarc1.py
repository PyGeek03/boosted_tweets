import os
import twarc
import json
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
client1 = twarc.Twarc(consumer_key, consumer_secret, access_token, access_token_secret)

#tweet_ids = ['1404353357469212673', '1404353618518499329']
#tweet_ids = ['1405295014327037956']
#data = {'data': list(client1.retweets(tweet_ids))}

world_trends = client1.trends_place(1)[0]["trends"]
for i in range(len(world_trends)):
    if world_trends[i]["tweet_volume"] is None:
        world_trends[i]["tweet_volume"] = 0
world_trends.sort(key=lambda trend: -trend["tweet_volume"])
data = {'data': world_trends}

serialized_json = json.dumps(data,
                             indent=4,
                             sort_keys=True)
print(serialized_json)
filename = input("Filename to output to: ")
with open(f'{filename}.json', 'w') as f:
    f.writelines(serialized_json)