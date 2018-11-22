from keys import keys
import tweetanalyzer
from tweepy import OAuthHandler
from tweepy import API
import os.path
from datetime import datetime

def run():
    # # # VARIABLES # # #
    charlie_pic_filename = 'media/charliespic.jpg'
    username = tweetanalyzer.get_username()
    tweet_id = tweetanalyzer.get_tweet_id()

    # # # # TWITTER UATHENTICATE # # # # 
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_SECRET = keys['access_token_secret']

    #OAuth process, using the keys and tokens
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)

    # # # TWITTER CLIENT # # # #
    class TwitterClient():
        def __init__(self, twitter_user=None): #default to none, which will default to host account
            self.auth = auth
            self.twitter_client = API(self.auth)
            self.twitter_user = twitter_user

    cliente = TwitterClient()

    if os.path.isfile(charlie_pic_filename) == True:
        current_time = str(datetime.now())
        message = 'Hey '+ username[1:] + ', thanks for my treat!'
        # cliente.twitter_client.update_status(str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'
        cliente.twitter_client.update_with_media(charlie_pic_filename,str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'
        os.remove(charlie_pic_filename)
        #os.remove(charlie_vid_filename)
    else:
        message = 'Hi ' + username[1:] + ', oh gah, so full.. send me a treat later!'
        cliente.twitter_client.update_status(str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'
