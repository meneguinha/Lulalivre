import os
import tweepy
import time
import random
import csv
import pathlib

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
    print(dict_aux)
    list_of_words = []
    list_of_words = text.split()
    print(list_of_words)
    link_to_post = 'Nada a declarar'
    for e in list_of_words:
        if e in dict_aux:
            elemento = str(e)
            link_to_post = dict_aux.get(elemento)
            print(link_to_post)
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
        print(text_tweet)
        response = phrase(text_tweet)
        api.update_status('@'+ tweet.user.screen_name + ' ' + response, in_reply_to_status_id=tweet.id)
        
    
def lula_dictionary():
    path = str(pathlib.Path(__file__).parent.resolve())
    print(path)
    slash = '/'
    archive_name = "lula_dictionary.csv"
    full_path = path + slash + archive_name

    with open(full_path, mode='r') as infile:
        reader = csv.reader(infile)
        with open('coors_new.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[0]:rows[1] for rows in reader}
    return mydict

dict_lula = lula_dictionary()
while True:
    _main_()
    time.sleep(60)
