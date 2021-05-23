from os import read, write
import tweepy
import time

api_key = '9pafozEx1svRzcMJ8KxTMY4lD'
api_secret_key = 'M6MzworadFoqrsFwxGZjLLx0RobAjyJ7DhEU5We6UDAc3rvs2L'
acess_key = '1394391405154476038-hWkTx6vnArqmlNeO20MExXHZgejb5U'
acess_secret = 'H0BzADfqBXSQ7jCiLcQDG2qsjDorh7zG7UJGK2HOQQgkt'
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
    tweets = api.search('terraplanista -filter:retweets', since_id =  read_last_seen_str, lang = 'pt')
    print('Último ID pesquisado:' + read_last_seen_str)
    for tweet in reversed(tweets):
        print(tweet.text)
        api.create_friendship(tweet.user.screen_name)
        api.retweet(tweet.id)
        store_last_seen(FILE_NAME, tweet.id)
        

while True:
    _main_()
    time.sleep(60)