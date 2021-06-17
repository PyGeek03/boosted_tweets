import botometer
import os
import json
from dotenv import load_dotenv

load_dotenv()

rapidapi_key = os.environ.get("RAPIDAPI_KEY")
twitter_app_auth = {
    'consumer_key': os.environ.get("CONSUMER_KEY"),
    'consumer_secret': os.environ.get("CONSUMER_SECRET"),
    'access_token': os.environ.get("ACCESS_TOKEN"),
    'access_token_secret': os.environ.get("ACCESS_TOKEN_SECRET")
    }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
# result = bom.check_account('@clayadavis')

# Check a single account by id
# result = bom.check_account(1548959833)

# Check a sequence of accounts
accounts = ["1312662813106724864"]
botometer_output = {screen_name: result for screen_name, result in bom.check_accounts_in(accounts)}
serialized_json = json.dumps(botometer_output,
                             indent=4,
                             sort_keys=True)
print(serialized_json)
filename = input("Filename to output to: ")
with open(f'{filename}.json', 'w') as f:
    f.writelines(serialized_json)