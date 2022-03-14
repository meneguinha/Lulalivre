# -*- coding: utf-8 -*-
import os
import tweepy
import time
import random
import csv
import pathlib
import datetime
import urllib.request

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
hours_to_update = [['07','00'],['08','00'], ['09','00'], ['10','00'], ['11','00'], ['12','00'], ['13','00'], ['14','00'],['15','00'] ,['16','00'],['17','00'],['18','00'],['19','00'],['20','00'],['21','00'],['22','00'],['23','00']]

while True:
    global dict_lula
    _main_()
    hour_minutes = str(datetime.datetime.now()).split()[1].split(':')
    del hour_minutes[-1]
    if hour_minutes in hours_to_update: 
        url = 'https://docs.google.com/spreadsheets/d/1rK5C5D4ll2r8zQ8QXP2Div9A3DdYaknDXCBxcGmYDyE/export?format=csv'
        urllib.request.urlretrieve(url)
        dict_lula = lula_dictionary()
        print('Tabela Atualizada às', datetime.datetime.now())
    time.sleep(60)