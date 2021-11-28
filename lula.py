from os import read, write, environ
import tweepy
import time

api_key = os.environ['api_key']
api_secret_key = os.environ['api_secret_key']
acess_key = os.environ['acess_key']
acess_secret = os.environ['acess_secret']
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(acess_key, acess_secret)

api = tweepy.API(auth)

FILE_NAME = 'last_seen.txt'

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def _main_():
    read_last_seen_str = str(read_last_seen(FILE_NAME))
    tweets = api.search('Lula -filter:retweets', since_id =  read_last_seen_str, lang = 'pt')
    print('Último ID pesquisado:' + read_last_seen_str)
    for tweet in reversed(tweets):
        print(tweet.text)
        #api.create_friendship(tweet.user.screen_name)
        api.retweet(tweet.id)
        store_last_seen(FILE_NAME, tweet.id)
        

while True:
    _main_()
    time.sleep(60)
