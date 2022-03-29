# -*- coding: utf-8 -*-
import os
import tweepy
import time
import pathlib
import pandas as pd

#FOR WINDOWS "\\" for linux "/"
#FOR HEROKU APP USE "/". DONT FORGET TO CHANGE

api_key = os.environ['api_key']
api_secret_key = os.environ['api_secret_key']
access_key = os.environ['access_token']
access_secret = os.environ['access_secret']
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
path_2 = str(pathlib.Path(__file__).parent.resolve())
slash_2 = '/'
archive_name_2 = "last_seen.txt"
full_path_2 = path_2 + slash_2 + archive_name_2
FILE_NAME = full_path_2


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

def phrase(text):
    global dict_lula
    dict_aux = dict_lula
    link_to_post = 'Nada a declarar'
    for key in dict_aux:
        if key in text:
            link_to_post = dict_aux.get(key)
            break
    return link_to_post

def _main_():
    read_last_seen_str = str(read_last_seen(FILE_NAME))
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode = 'extended')
    print('Ultimo ID pesquisado:' + read_last_seen_str)
    for tweet in reversed(tweets):
        store_last_seen(FILE_NAME, tweet.id)
        text_tweet = tweet.full_text
        text_tweet = text_tweet.lower()
        response = phrase(text_tweet)
        try:
            api.update_status('@'+ tweet.user.screen_name + ' ' + response, in_reply_to_status_id=tweet.id)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(5)
        
    
def lula_dictionary():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/1rK5C5D4ll2r8zQ8QXP2Div9A3DdYaknDXCBxcGmYDyE/export?format=csv")
    mydict = dict(zip(list(df.assunto), list(df.link)))
    return mydict

dict_lula = lula_dictionary()

while True:
    _main_()
    dict_lula = lula_dictionary()
    time.sleep(60)
