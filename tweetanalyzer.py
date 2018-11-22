import json

# # # VARIABLES # # #
fetched_tweets_filename = "files/tweets.json"

def get_username():
    with open(fetched_tweets_filename, 'r') as rf:
        data = json.load(rf)
    sender_username = '@'+str(data["user"]["screen_name"])
    return sender_username

def get_tweet_id():
    with open(fetched_tweets_filename,'r') as rf:
        data = json.load(rf)
    tweet_id = str(data["id"])
    return tweet_id

