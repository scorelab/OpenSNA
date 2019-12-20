import sys
import tweepy
import os
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

name = '' #Twitter account screen_name

replies = []

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=name, timeout=999999).items(10):
    for tweet in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if tweet.in_reply_to_status_id_str == full_tweets.id_str:
                replies.append(tweet.text)
                replies.append(tweet.user.screen_name)

    print("Tweet :", full_tweets.text.translate(non_bmp_map))

    analysis = TextBlob(full_tweets.text)
    print(analysis.sentiment)
    print("")

    for elements in replies:
        print("Replies :", elements)
        analysis = TextBlob(elements)
        print(analysis.sentiment)
        print("")
    replies.clear()

    print("")
