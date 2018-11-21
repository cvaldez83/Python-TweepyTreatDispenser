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
fetched_tweets_filename = "tweets.json"
debug_filename = 'debug.json'
listen_to_userID = ['1059557863775850496'] # reats4charlie user id
charlie_pic_filename = 'charliespic.jpg'
charlie_vid_filename = 'charliedetected.mp4'

# # # # TWITTER UATHENTICATE # # # # 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_SECRET = keys['access_token_secret']

#OAuth process, using the keys and tokens
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)

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

# # # # TWITTER LISTENER # # # # 
class StdOutListener(StreamListener):
        
    def on_data(self,data):
        print('Someone tweeted to @treats4charlie.')
        # # # WRITE TWEET TO FILE # # #
        with open(fetched_tweets_filename, 'w') as tf:
            print('Writing tweet to: ' + fetched_tweets_filename)
            tf.write(data)
        with open(debug_filename, 'a') as tf:
            print('Writing same tweet to debug.json')
            tf.write(data)
        username = get_username()
        tweet_id = get_tweet_id()
        
        # # # CREATE CLIENT TO SEND RESPONSE # # # 
        if username != "@treats4charlie":
            print('senders username: '+ username)
            print('tweet id: ' + tweet_id)
            
            # # Run ondata.py # #
            ondata.run()
            
            # Run TwitterClient
            print('creating TwitterClient: cliente')
            cliente = TwitterClient()
            print('cliente created. sending response tweet...')

            # # # CREATE CLIENT TO SEND RESPONSE # # # 
            # if os.path.isfile(charlie_vid_filename) == True:
            if os.path.isfile(charlie_pic_filename) == True:
                current_time = str(datetime.now())
                message = 'Hey '+ username[1:] + ', thanks for my treat!'
                # cliente.twitter_client.update_status(str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'
                cliente.twitter_client.update_with_media(charlie_pic_filename,str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'
                os.remove(charlie_pic_filename)
                os.remove(charlie_vid_filename)
            else:
                message = 'Hi ' + username[1:] + ', oh gah, so full.. send me a treat later!'
                cliente.twitter_client.update_status(str(username) + ' ' + message, tweet_id) # previous tweet id '1061689337312567296'

        else:
            print('tweet ignored since it was from charlie')
        return True

    def on_status(self,data):
        return True

    def on_error(self,status):
        print('error: ' + status)

# # # TWITTER CLIENT # # # #
class TwitterClient():
    def __init__(self, twitter_user=None): #default to none, which will default to my own account
        self.auth = auth
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

if __name__ == '__main__':
    # # # # CREATE LISTENER OBJECT # # # 
    listener = StdOutListener()
    stream = Stream(auth,listener)
    stream.filter(follow=listen_to_userID)
    
    # # DELETE # #
    #send response tweet
    #message = 'hellooooo auto response from python!'
    # username = '@cvaldez83'
    #print('creating cliente')
    #cliente = TwitterClient()
    #print('sending response tweet')
    #cliente.twitter_client.update_status(str(get_username()) + ' ' + message)
    #print(get_username())