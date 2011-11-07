import sqlite3 as sqlite
import db
from twitter_api import get_api
import datetime

con = db.get_connection()
cursor = con.cursor()
api = get_api()
class TwitterUser():
    def __init__(self, user_id, user_id_str, scrn_name, name,
            foer_cnt, foer_ids, friend_cnt, friend_ids, 
            desc, location, created_at, status_cnt, verified,
            scanned):
        self.user_id = user_id
        self.user_id_str = user_id_str
        self.scrn_name = scrn_name
        self.name = name
        self.foer_cnt = foer_cnt
        self.foer_ids = ",".join([str(i) for i in foer_ids])
        self.friend_cnt = friend_cnt
        self.friend_ids = ",".join([str(i) for i in friend_ids])
        self.desc = desc
        self.location = location
        if isinstance(created_at, datetime.datetime):
            self.created_at = created_at.date()
        else:
            self.created_at = created_at
        self.status_cnt = status_cnt
        self.verified = verified
        self.scanned = scanned

    @classmethod
    def save_tweepy_user(cls, tweepy):
        user = TwitterUser(tweepy.id, tweepy.id_str, tweepy.screen_name, tweepy.name,
                tweepy.followers_count, tweepy.followers_ids(),
                tweepy.friends_count, api.friends_ids(tweepy.id), tweepy.description,
                tweepy.location, tweepy.created_at, tweepy.statuses_count,
                tweepy.verified, False)
        user.save_new()
        return user

    @property
    def tweepy_obj(self):
        return api.get_user(self.user_id)

    def save_new(self):
        self.scanned = False
        info = (self.user_id, self.user_id_str, self.scrn_name, self.name,
                self.foer_cnt, self.foer_ids, self.friend_cnt,
                self.friend_ids, self.desc, self.location,
                self.created_at, self.status_cnt, self.verified, self.scanned)
        try:
            cursor.execute('''insert into t_user(user_id, user_id_str,
            screen_name, name, foer_cnt, foer_ids, friend_cnt,
            friend_ids, desc, location, created_at, status_cnt,
            verified, scanned) values 
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', info)
            con.commit()
        except sqlite.IntegrityError:
            print "can not save user", self.user_id, "(",self.scrn_name,") to the database"

    @property
    def id(self):
        try:
            cursor.execute('''select id from t_user where user_id =
                    ?''',(self.user_id,))
            id = cursor.fetchone()[0]
        except sqlite.IntegrityError:
            print "can not find user ", self.user_id, "(",
            self.scrn_name, ") , it's not in database"
            id = 0
        return id

    def update(self):
        info = (self.user_id, self.user_id_str, self.scrn_name, self.name,
                self.foer_cnt, self.foer_ids, self.friend_cnt,
                self.friend_ids, self.desc, self.location, self.created_at,
                self.status_cnt, self.verified, self.scanned, self.id)
        try:
            cursor.execute('''update t_user set user_id=?, user_id_str=?,
            screen_name=?, name=?, foer_cnt=?, foer_ids=?,
            friend_cnt=?, friend_ids=?, desc=?,
            location=?, created_at=?, status_cnt=?, verified=?,
            scanned=? where id=?''', info)
            con.commit()
        except sqlite.IntegrityError:
            print "can not update user", self.user_id, "(",self.scrn_name,") to the database"
        pass

    def update_scanned(self):
        self.scanned = True
        try:
            cursor.execute('''update t_user set scanned=? where
                    user_id=?''', (self.scanned, self.user_id))
            con.commit()
        except sqlite.InternalError:
            print "can not update ", self.user_id, "(",self.screen_name,") to scanned"

    @classmethod
    def get_by_id(cls, twitter_id):
        cursor.execute('''select user_id, user_id_str,
            screen_name, name, foer_cnt, foer_ids, friend_cnt,
            friend_ids, desc, location, created_at, 
            status_cnt, verified, scanned from t_user
            where user_id = ?''', (twitter_id,))
        result = cursor.fetchone()
        if result:
            t_user = TwitterUser(*result)
            return t_user
        else: return None

    @classmethod
    def get_next_unscanned(cls):
        cursor.execute('''select user_id, user_id_str,
            screen_name, name, foer_cnt, foer_ids, friend_cnt,
            friend_ids, desc, location, created_at, 
            status_cnt, verified, scanned from t_user
            where scanned=0 limit 0,1''')
        result = cursor.fetchone()
        if result:
            t_user = TwitterUser(*result)
            return t_user
        else: return None