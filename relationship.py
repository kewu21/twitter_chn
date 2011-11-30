import oauth2 as oauth
from twitter_api import consumer_key, consumer_secret, access_token, access_token_secret 

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

# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=consumer_key, 
            secret=consumer_secret)

# Request token URL for Twitter.
request_token_url = "https://twitter.com/oauth/request_token"

# Create our client.
client = oauth.Client(consumer)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url, "GET")
print resp
print content
'''
