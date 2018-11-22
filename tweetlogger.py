
# # # VARIABLES # # #
fetched_tweets_filename = "files/tweets.json"
debug_filename = 'files/debug.json'

def write_tweet_to_file(data):
    with open(fetched_tweets_filename, 'w') as tf:
        print('Writing tweet to: ' + fetched_tweets_filename)
        tf.write(data)
    with open(debug_filename, 'a') as tf:
        print('Writing same tweet to debug.json')
        tf.write(data)