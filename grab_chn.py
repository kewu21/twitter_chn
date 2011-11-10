#!/user/bin/env python
from tweepy import TweepError
from twitter_api import get_api2
from tweepy import Cursor
from time import sleep
from twitter_user import TwitterUser
import re
import db
from db import save_non_chn, is_in_no_chn

api = get_api2()
chn_search = re.compile(ur"[\u4e00-\u9fa5]").search
jpn_search = re.compile(ur"[\u3040-\u309F\u30A0-\u30FF]").search
krn_search = re.compile(ur"[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]").search

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
    try:
        c = Cursor(api.followers,user.user_id)
    except TweepError:
        print "tweep breaks!"
        print TweepError.message
    while(True):
        try:
            print 'taking a rest before move to next page'
            sleep(10)
            page = c.pages().next()
            print "start a new page of user ", user.scrn_name, \
                'page', c.pages().count
        except TweepError:
            print "tweep breaks!"
            print TweepError.message
            continue
        except StopIteration:
            print "Move to next unscanned"
            break
        
        for tweepy_user in page:
            print "follower -----", tweepy_user.screen_name, "----- found......"
            if TwitterUser.get_by_id(tweepy_user.id) or \
                is_in_no_chn(tweepy_user.id):
                print 'ALREADY in DB!!, skip'
                continue
            try:
                if not tweepy_user.protected or \
                        (tweepy_user.protected and tweepy_user.following):
                        if is_chn(tweepy_user):
                            print "and speaks Chinese! Saving...."
                            TwitterUser.save_tweepy_user(tweepy_user)
                        else:
                            save_non_chn(tweepy_user.id)
                            print "pitty, s/he is not Chinese Speaker, next..."
                            continue
            except TweepError:
                print "tweep breaks!"
                print TweepError.message
            try:
                print "the remaining hit is ", \
                    api.rate_limit_status()['remaining_hits']
            except TweepError:
                print "tweep breaks!"
                print TweepError.message
        page =[]
    user.update_scanned()

def is_chn_by_timeline(tweepy_user):
    print 'has to check timeline...'
    is_chn = False
    try:
        for status in tweepy_user.timeline():
            if text_is_chn(status.text):
                print 'chinese!!!', status.text
                is_chn = True
                print is_chn
                break
    except TweepError:
        print "tweep breaks!"
        print TweepError.message
    print 'taking a rest'
    sleep(10)
    return is_chn

def is_chn(tweepy_user):
    print 'Check if speak Chinese..'
    is_chn = False
    is_jpn = False
    is_krn = False
    print 'checking most recent status...'
    if hasattr(tweepy_user, 'status'):
        if text_is_chn(tweepy_user.status.text):
            is_chn = True
        elif jpn_search(tweepy_user.status.text):
            print "has jpn word!"
            is_jpn = True
        elif krn_search(tweepy_user.status.text):
            print "has krn word!"
            is_krn = True
    print 'trying user description'
    if hasattr(tweepy_user, 'description') and tweepy_user.description:
        if text_is_chn(tweepy_user.description):
            is_chn = True
        elif jpn_search(tweepy_user.description):
            print "has jpn word!"
            is_jpn = True
        elif krn_search(tweepy_user.description):
            print "has krn word!"
            is_krn = True
    print 'Checking name...'
    if text_is_chn(tweepy_user.name):
        print 'Chinese name!'
        is_chn = True
    if tweepy_user.statuses_count > 10 and not is_chn \
        and not is_jpn and not is_krn:
        is_chn = is_chn_by_timeline(tweepy_user)
    return (is_chn and not is_jpn and not is_krn)

def text_is_chn(text):
    if chn_search(text) and not jpn_search(text) and not \
        krn_search(text):
        return True
    else: return False

if __name__ == "__main__":
    fetch()
