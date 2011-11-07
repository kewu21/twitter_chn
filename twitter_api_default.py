#!/user/bin/env python
import tweepy


consumer_key='your c key'
consumer_secret='your c secret'
access_token='your a token'
access_token_secret='your a token secret'

def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

