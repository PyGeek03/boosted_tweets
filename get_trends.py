import os
import twarc
import json
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
client1 = twarc.Twarc(consumer_key, consumer_secret,
                      access_token, access_token_secret)

location_codes = {
    'world': 1, 
    'US': 23424977
    }
chosen_location = 'US'
trends = client1.trends_place(location_codes[chosen_location])[0]["trends"]
for i in range(len(trends)):
    if trends[i]["tweet_volume"] is None:
        trends[i]["tweet_volume"] = 0
trends.sort(key=lambda trend: -trend["tweet_volume"])
data = {'data': trends}

serialized_json = json.dumps(data,
                             indent=4,
                             sort_keys=True)
print(serialized_json)
filename = input("Filename to output to: ")
with open(f'{filename}.json', 'w') as f:
    f.writelines(serialized_json)
