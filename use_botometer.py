import botometer
import os
import json
import argparse

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
#accounts = ["1312662813106724864"]
#conversation_json_file = "schumer_tweet-full_conversation-1405321025861165060.json"

parser = argparse.ArgumentParser(
    description='Use Botometer API to check new accounts.'
)
parser.add_argument('conversation_files', metavar='[FILE]', type=str, nargs='+',
                    help=("one or more json files, each file consisting of "
                          "the whole conversation associated with a Tweet")
)

parser.add_argument('--dry', dest='dry_run', action='store_true',
                    help='make a dry run (without using the API)')

args = parser.parse_args()

accounts = set()
for file in args.conversation_files:
    with open(file, 'r') as f:
        data = json.load(f)
    tweets = data["data"]
    accounts |= set(tweet["author_id"] for tweet in tweets)  # Twitter API v2

output_file = "outputs/botometer_cache.json"

with open(output_file, 'r') as f:
    all_output = json.load(f)
prev_accounts = set(all_output)

new_accounts = accounts - prev_accounts

if args.dry_run:
    print(new_accounts)
    print(len(new_accounts))
else:
    if len(new_accounts) > 2000:  # Botometer API's free daily limit
        new_accounts = set(list(new_accounts)[:2000])

    new_output = {screen_name: result for screen_name, result in bom.check_accounts_in(new_accounts)}
    [print(f"{k}: {v}") for k, v in new_output.items()]
    print(f"Num. of new accounts added: {len(new_accounts)}")
    all_output.update(new_output)
    serialized_json = json.dumps(all_output,
                                indent=4,
                                sort_keys=True)

    print(f"Total num. of accounts checked: {len(all_output)}")
    
    with open(output_file, 'w') as f:
        f.writelines(serialized_json)