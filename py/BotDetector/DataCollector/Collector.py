'''
Created on 15 may. 2018

@author: Santirrium
'''

import csv
import time
import re
import codecs
from io import StringIO
from argparse import ArgumentParser
import tweepy
from tweepy import OAuthHandler
import threading
import logging

from py.BotDetector.others import utils
from py.BotDetector.DataCollector.DBmanager import DBmanager
from py.BotDetector.DataCollector.TwUsers import TwUser
from py.BotDetector.DataCollector.Bot_detector import BotDetector

#Set log
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("tweepy").setLevel(logging.WARNING)
logging.basicConfig(
    filename='bot_detector.log', 
    level=logging.INFO, 
    format="%(asctime)s:%(threadName)10s:%(levelname)s: %(message)s", datefmt='%d/%m/%Y %I:%M:%S %p')

def hilo_process(following_part, credential, dbm, twitter_account, start_time):
    
    logging.info('Soy el hilo {} iniciadose'.format(threading.current_thread().getName()))
    thread_name = threading.current_thread().getName()
    
    consumer_key = credential['consumer_key']
    consumer_secret  = credential['consumer_secret']
    access_token  = credential['access_token']
    access_secret  = credential['access_secret']
    
    #twitter connection api
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    #Inicializet object bot detector
    bot_detector = BotDetector(api)
    
    #process the following_part
    for i, user in enumerate(following_part):
       
        logging.info('[{}][{}]Usuario:{}'.format(thread_name, i, user.screen_name))
        twuser = ''
        twuser = TwUser(twitter_account,
                        utils.clear(user.name),  
                        utils.clear(user.screen_name), 
                        user.location, 
                        user.url, 
                        user.protected, 
                        user.followers_count, 
                        user.friends_count, 
                        user.listed_count, 
                        user.favourites_count, 
                        user.statuses_count, 
                        user.created_at, 
                        user.utc_offset, 
                        user.profile_background_color, 
                        user.profile_background_image_url,
                        user.profile_background_image_url_https,
                        user.profile_background_tile,
                        utils.getattribute(user, 'profile_banner_url'),
                        user.profile_image_url,
                        user.profile_image_url_https,
                        user.profile_link_color,
                        user.profile_sidebar_border_color,
                        user.profile_sidebar_fill_color,
                        user.profile_text_color,
                        user.profile_use_background_image,
                        user.default_profile,
                        user.default_profile_image,
                        utils.getattribute(user, 'withheld_in_countries'),
                        utils.getattribute(user, 'withheld_scope'),
                        utils.clear(user.description), 
                        bot_detector.creation_date(user.created_at),
                        bot_detector.is_retweet_bot(user.screen_name), 
                        bot_detector.default_twitter_account(user), 
                        bot_detector.location(user), 
                        bot_detector.followers_ratio(user),
                        bot_detector.format_name(user.name)
                        )
        dbm.save_record(twuser.ToDbJson())
        
    logging.info('Hilo {} finalizando, tiempo total: {} Minutos'.format(thread_name, (time.time() - start_time)/60))

def get_friends_descriptions(api_credentials, twitter_account, max_users, start_time):
    """
    Return the bios of the people that a user follows

    api_credentials -- the tweetpy API credentials to create API object
    twitter_account -- the Twitter handle of the user
    max_users -- the maximum amount of users to return
    """
    #extract the first credencial
    first_credential = api_credentials.pop(0)
    
    consumer_key = first_credential['consumer_key']
    consumer_secret  = first_credential['consumer_secret']
    access_token  = first_credential['access_token']
    access_secret  = first_credential['access_secret']
    
    #twitter connection api
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    

    user_ids = []

    try:
        for page in tweepy.Cursor(api.followers_ids, id=twitter_account, count=5000).pages():
            user_ids.extend(page)

    except tweepy.RateLimitError:
        logging.info ("RateLimitError...waiting 1000 seconds to continue")
        time.sleep(1000)
        for page in tweepy.Cursor(api.followers_ids, id=twitter_account, count=5000).pages():
            user_ids.extend(page)

    following = []

    for start in range(0, min(max_users, len(user_ids)), 100):
        end = start + 100

        try:
            following.extend(api.lookup_users(user_ids[start:end]))

        except tweepy.RateLimitError:
            logging.info ("RateLimitError...waiting 1000 seconds to continue")
            time.sleep(1000)
            following.extend(api.lookup_users(user_ids[start:end]))
    
    c_following = len(following)
    logging.info('Encontramos {} seguidores'.format(c_following))
    #Instance of bot_detector
    #bot_detector = BotDetector(api)
       
    #Conexion a la BD BotDetecto
    dbm = DBmanager('TwUsers-Test')
    
    #N threads
    n_threads = 14
    
    #calc divisions
    split = c_following // n_threads
    init = 0
    end = split - 1
    
    #run the fucking threads
    for n in range(n_threads):
        
        if (n == n_threads - 1):
            end = c_following - 1
        
        hilo = threading.Thread(name='Hilo%s' %n, 
                                target=hilo_process, 
                                args=(following[init:end], api_credentials[n], dbm, twitter_account,start_time,))
        
        hilo.start()
        
        init = end + 1
        end = end + split - 1
    
    logging.info('Terminaron los hilos?')
    
    
if __name__ == "__main__":
    #Set start time
    start_time = time.time()
    
    #load the inicial configuration 
    configuration = utils.get_config(config_file = 'config.json')


    TWITTER_ACCOUNT = "jualtorres"
    MAX_USERS = configuration['max_user']
    api_credentials = configuration['api_twitter']

    logging.info ("Colectando datos...")
    logging.info ("Cuenta: @" + TWITTER_ACCOUNT)
    get_friends_descriptions(api_credentials, TWITTER_ACCOUNT, MAX_USERS, start_time)
    
    #logging.info("Fin..")
    #logging.info("--- %s Minutos ---" % ((time.time() - start_time)/60))