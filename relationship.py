from twitter_user import TwitterUser
from tweepy import Cursor, TweepError
from time import sleep
from twitter_api import get_api2 as get_api


TOP_100 = TwitterUser.get_top_100_by_foer()
api = get_api()

def get_follower_ids(tweepy_obj):
    ids_list = []
    try:
        c = Cursor(api.followers_ids, tweepy_obj.id)
    except TweepError:
        print 'tweepy breaks!'
    while(True):
        try:
            print 'new page...'
            page = c.pages().next()
            sleep(2)
        except TweepError:
            print "tweep breaks!"
        except StopIteration:
            print 'done with', tweepy_obj.id
            break
        ids_list.extend(page)
        
    try:
        print "the remaining hit is ", \
            api.rate_limit_status()['remaining_hits']
    except TweepError:
        print "tweep breaks!"
        print TweepError.message
    return ids_list

def get_relation(top_list):
    for twitter_id in top_list:
        print twitter_id, 'analyzing.....'
        sleep(3)
        print 'getting followers id...'
        twitter_user = TwitterUser.get_by_id(twitter_id)
        try:
            tweepy_obj = twitter_user.tweepy_obj
            foer_ids = get_follower_ids(tweepy_obj)
            api.rate_limit_status()['remaining_hits']
            top_100_foer = list(set(foer_ids).intersection(TOP_100))
            print 'saving relation....'
            for id in top_100_foer:
                TwitterUser.save_relationship(twitter_id, id)
        except TweepError:
            print "tweep breaks!"
            print TweepError.message

if __name__ == '__main__':
    list_to_check = [id for id in TOP_100 if id not in
            TwitterUser.get_existing_relation_leading()]
    get_relation(list_to_check)

'''
# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=consumer_key, 
            secret=consumer_secret)

# Request token URL for Twitter.
request_token_url = "https://api.twitter.com/1/friendships/lookup.json?user_id=783214,6253282,"
token = oauth.Token(key=access_token, secret=access_token_secret)

# Create our client.
client = oauth.Client(consumer, token)


# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url, "GET")
print resp
print content
'''
