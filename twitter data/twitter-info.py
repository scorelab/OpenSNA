import tweepy
import os
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_key = os.getenv('access_key')
access_secret = os.getenv('access_secret')

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='politics_tweets', ignore=400)


def get_all_tweets(screen_name):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        #id = [(tweet.id_str) for tweet in alltweets]

        #html = requests.get("https://twitter.com/%s/status/%s" % ("GotabayaR", id[1]))
        #soup = BeautifulSoup(html.text, 'lxml')

        #comments = soup.find_all('span', attrs={'class': 'ProfileTweet-actionCountForAria'})[0].contents

    outtweets = [{'ID': tweet.id_str, 'Text': tweet.text, 'Date': tweet.created_at, 'author': tweet.user.screen_name,
                  'retweet-count': tweet.retweet_count, 'favourites-count': tweet.favorite_count, 'language': tweet.lang}
                 for tweet in alltweets]

    def save_es(outtweets, es):  # Peps8 convention
        data = [  # Please without s in data
            {
                "_index": "politics_tweets",
                "_type": "GR",
                "_id": index,
                "_source": ID
            }
            for index, ID in enumerate(outtweets)
        ]
        helpers.bulk(es, data)

    save_es(outtweets, es)

    print(outtweets)
    print('\n')


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("GotabayaR")
