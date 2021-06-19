import botometer
import os
import json
import argparse
from collections import Counter

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

parser.add_argument('--max', dest='max_calls', type=int, default=2000,
                        help=("maximum number of Botometer API calls "
                              "(default: 2000, which is Botometer API's free daily limit); "
                              "priority will be given to the original tweet's author, "
                              "and then the most frequently appeared accounts"))

args = parser.parse_args()

all_accounts = Counter()
for file in args.conversation_files:
    with open(file, 'r') as f:
        data = json.load(f)
    tweets = data["data"]
    tweets.sort(key=lambda t: t['id'])
    orig_author = tweets[0]["author_id"]
    all_accounts[orig_author] = float('inf')
    all_accounts |= Counter(tweet["author_id"] for tweet in tweets)  # Twitter API v2

output_file = "outputs/botometer_cache.json"

with open(output_file, 'r') as f:
    checked_accounts = json.load(f)

for acc in checked_accounts:
    if acc in all_accounts:
        all_accounts[acc] = 0

unchecked_accounts = all_accounts.most_common(args.max_calls)
new_accounts = list(k for k, v in unchecked_accounts if v > 0)
#if len(new_accounts) > args.max_calls:
#    new_accounts = set(list(new_accounts)[:args.max_calls])

if args.dry_run:
    print(all_accounts.most_common(args.max_calls))
    print(len(new_accounts))
else:
    count = 0
    try:
        for screen_name, result in bom.check_accounts_in(new_accounts):
            checked_accounts[screen_name] = result
            count += 1
            print(f"Checked {count} accounts\n")
            print(f"{screen_name}: {result}\n")
    except KeyboardInterrupt:  # gracefully exit if user presses Ctrl-C
        print()

    #[print(f"{k}: {v}\n") for k, v in new_output.items()]
    print(f"Num. of new accounts added: {count}")

    serialized_json = json.dumps(checked_accounts,
                                indent=4,
                                sort_keys=True)

    print(f"Total num. of accounts checked: {len(checked_accounts)}")
    
    with open(output_file, 'w') as f:
        f.writelines(serialized_json)