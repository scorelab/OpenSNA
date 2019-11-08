import csv
import tweepy
import os
import requests
from elasticsearch import Elasticsearch, helpers
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='reply', ignore=400)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

name = 'MaithripalaS'
tweet_id = '1188793444933595137'

html = requests.get("https://twitter.com/%s/status/%s" % (name, tweet_id))
soup = BeautifulSoup(html.text, 'lxml')

comments = soup.find_all('span', attrs={'class': 'ProfileTweet-actionCountForAria'})[0].contents

replies = []
for tweet in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=5).items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)

reply = [{'Reply-count': comments, 'Name': tweet.user.screen_name, 'Reply': tweet.text} for tweet in replies]


def save_es(reply, es):  # Peps8 convention
    data = [  # Please without s in data
        {
            "_index": "reply",
            "_type": "GR",
            "_id": index,
            "_source": ID
        }
        for index, ID in enumerate(reply)
    ]
    helpers.bulk(es, data)


save_es(reply, es)

print(reply)
