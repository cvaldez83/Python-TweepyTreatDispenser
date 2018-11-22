import tweetresponse
import tweetlogger
import tweetanalyzer
import ondata
import json
import time
import os
import os.path
from keys import keys
from datetime import datetime
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

# # # # VARIABLES # # # # 
host_username = '@treats4charlie'
listen_to_userID = ['1059557863775850496'] # reats4charlie user id
charlie_pic_filename = 'media/charliespic.jpg'
charlie_vid_filename = 'media/charliedetected.mp4'

# # # # TWITTER UATHENTICATE # # # # 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_SECRET = keys['access_token_secret']

#OAuth process, using the keys and tokens
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)

# # # # TWITTER LISTENER # # # # 
class StdOutListener(StreamListener):
        
    def on_data(self,data):
        print('Someone sent tweet to ' + host_username)
        # # # WRITE TWEET TO FILE # # #
        tweetlogger.write_tweet_to_file(data)
        username = tweetanalyzer.get_username()
        tweet_id = tweetanalyzer.get_tweet_id()
        
        # things to do if unique user 
        if username != host_username:
            print('senders username: '+ username)
            print('senders tweet id: ' + tweet_id)
            ondata.run()
            tweetresponse.run()

        else:
            print('tweet ignored since it was from ' + host_username)
        return True

    def on_status(self,data):
        return True

    def on_error(self,status):
        print('error: ' + status)

if __name__ == '__main__':
    # # # # CREATE LISTENER OBJECT # # # 
    listener = StdOutListener()
    stream = Stream(auth,listener)
    stream.filter(follow=listen_to_userID)