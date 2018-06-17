import json
import tweepy
import datetime
import re
from dateutil.relativedelta import relativedelta
from py.BotDetector.DataCollector.DBmanager import DBmanager
from _overlapped import NULL


class BotDetector:
    __api = None
    __conf = None
    __analyzed_features = 8

    def __init__(self, api):
        if(api):
            self.__api = api
        else:
            #Credenciales de twitter 
            consumer_key = '4qFYcgtelubwkBlJaYlPYlEpa'
            consumer_secret = 'HRSUwg5QFi0rnizqNYwIgSy4CE47pVjab8PjchIppzB60jVC9U'
            access_token = '65257006-tO6cC5TVGSPmpzI3a9LO1oUEmFbKtAdY2gs9wLFnO'
            access_secret = 'E6VuPitApOi6yqYm2XgmZlBKa2BkMl7OpnkksOuNYwyUq'
          
            #twitter connection api
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            self.__api = tweepy.API(
                auth,
                wait_on_rate_limit=True,
                wait_on_rate_limit_notify=True)

    def __parse_date(self, date):
        split_date = date.split(' ')
        date = {'date': ' '.join(split_date[0:3]), 'time': split_date[3],
                'year': split_date[5]}
        return date

    # Get tweets in the timeline of a given user
    def __get_timeline(self, user):
        timeline = []
        
        try:
            for status in tweepy.Cursor(self.__api.user_timeline, screen_name=user).items(100):
                timeline_data = {'tweet_creation': status._json['created_at'],
                                 'text': status._json['text']}
                timeline.append(timeline_data)
        except tweepy.TweepError:
            print("No pudimos obtener el timeline de" + user)
        return timeline

    # Check when the account was created
    def creation_date(self, creation):
        
        difference_in_years = relativedelta(datetime.datetime.now(), creation).years

        if difference_in_years < 1:
            return 1
        else:
            return 0

    # Check the number of retweets in a given timeline
    # return True if the number of retweets is greater or equal
    # than a defined threshold (e.g., 90%), False otherwise
    def is_retweet_bot(self, user):
        num_tweets = 0
        num_rts = 0
        per_rts = 0
        threshold = 90
        
        #get timeline
        timeline = self.__get_timeline(user)
        
        for tweet in timeline:
            num_tweets += 1
            if 'RT' in tweet['text']:
                num_rts += 1
        
        #prevent division by zero
        if(num_tweets != 0):
            per_rts = (100*num_rts)/num_tweets
        
        if per_rts >= threshold:
            return True
        else:
            return False

    # Check the presence/absent of default elements in the profile of a given user
    def default_twitter_account(self, user):
        count = 0
        # Default twitter profile
        if user.default_profile is True:
            count += 1
        # Default profile image
        if user.default_profile_image is True:
            count += 1
        # Background image
        if user.profile_use_background_image is False:
            count += 1
        # None description
        if user.description == '':
            count += 1
        return count

    # Check the absence of geographical metadata in the profile of a given user
    def location(self, user):
        if user.location == '':
            return 1
        else:
            return 0

    # Compute the ratio between followers/friends of a given user
    def followers_ratio(self, user):
        ratio = int(user.followers_count)/int(user.friends_count)
        if ratio < 0.4:
            return 1
        else:
            return 0


    def format_name(self, user):
        pattern = '^[A-Za-z]{1,15}[0-9]{3,12}$'
        prog = re.compile(pattern)
        
        result = prog.match(user)
        
        if result != None:
            return 1
        else:
            return 0
    
    def compute_bot_probability(self, users):
        for user in users:
            bot_score = 0
            print('Computing the probability of the user {0}'.format(user))
            # Get information about the user, check
            # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
            # to understand the data of users available in the tweet
            # objects
            #data = self.__get_user(user)
            # Using the Twitter API get tweets of the user's timeline
            #timeline = self.__get_timeline(user)
            # Check heuristics
            #bot_score += self.__is_retweet_bot(timeline)
            #bot_score += self.format_name(user)
            #bot_score = bot_score + self.__creation_date(self.__parse_date(data['created_at']),
            #                                             self.__conf['current_year'])
            #bot_score = bot_score + self.__default_twitter_account(data)
            #bot_score = bot_score + self.__location(data)
            #bot_score = bot_score + self.__followers_ratio(data)
            print('There are a {0}% of probability that the user {1} would be bot'.format(
                  round((bot_score/self.__analyzed_features)*100, 2), user))


if __name__ == "__main__":
    

    users = ['Sandra523515']
    bot_detector = BotDetector(NULL)
    bot_detector.compute_bot_probability(users)
