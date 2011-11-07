#!/user/bin/env python
from tweepy import TweepError
from twitter_api import get_api
from tweepy import Cursor
from time import sleep
from twitter_user import TwitterUser
import re
import db

api = get_api()
chn_search = re.compile(ur"[\u4e00-\u9fa5]").search
jpn_search = re.compile(ur"[\u3040-\u309F\u30A0-\u30FF]").search

def init():
    db.init()
    first_user = api.me()
    TwitterUser.save_tweepy_user(first_user)

def fetch():
    current_user = TwitterUser.get_next_unscanned()
    if current_user:
        print "analyzing ", current_user.scrn_name, "......"
        save_user_followers(current_user)
        fetch()
    else:
        print "done!"

def save_user_followers(user):
    c = Cursor(api.followers,user.user_id)
    for page in c.pages():
        print "start a new page of user ", user.scrn_name
        for tweepy_user in page:
            print "follower ", tweepy_user.screen_name, " found......"
            if not tweepy_user.protected:
                try:
                    if is_chn(tweepy_user):
                        print "and speaks Chinese! Saving...."
                        TwitterUser.save_tweepy_user(tweepy_user)
                    else:
                        print "pitty, s/he is not Chinese Speaker, next..."
                        continue
                except TweepError:
                    print "tweep breaks!"
                    raise
        sleep(15)
    user.update_scanned()

def is_chn_by_timeline(tweepy_user):
    print 'has to check timeline...'
    is_chn = False
    for status in tweepy_user.timeline():
        if text_is_chn(stauts.text):
            is_chn = True
            break
    print 'taking a rest'
    sleep(11)
    return is_chn

def is_chn(tweepy_user):
    print 'Check if speak Chinese..'
    is_chn = False
    if hasattr(tweepy_user, 'status'):
        print 'checking most recent status...'
        if text_is_chn(tweepy_user.status.text):
            is_chn = True
    elif hasattr(tweepy_user, 'description'):
        print 'trying user description'
        if text_is_chn(tweepy_user.description):
            is_chn = True
    elif tweepy_user.statuses_count > 10:
        is_chn = is_chn_by_timeline(tweepy_user)

    return is_chn

def text_is_chn(text):
    if chn_search(text) and not jpn_search(text):
        return True
    else: return False

if __name__ == "__main__":
    fetch()
