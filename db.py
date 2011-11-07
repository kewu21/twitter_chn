import sqlite3 as sqlite

DATABASE = 'networks'

def init():
    """docstring for init"""
    con = get_connection()
    cursor = con.cursor()
    create_twitter_user(cursor)
    create_twitter_relation(cursor)
    con.commit()
    cursor.close()

def create_twitter_user(cursor):
    try:
        cursor.execute('''drop table if exists t_user''')
        cursor.execute('''create table t_user 
            (id integer primary key autoincrement,
            user_id integer unique not null,
            user_id_str text unique not null,
            screen_name text not null,
            name text not null,
            foer_cnt integer not null,
            foer_ids text,
            friend_cnt integer not null,
            friend_ids text,
            desc text,
            location text,
            created_at date not null,
            status_cnt integer not null,
            verified integer,
            scanned integer)''')
    except sqlite.InterfaceError:
        print "can't create table t_user"


def create_twitter_relation(cursor):
    try:
        cursor.execute('''drop table if exists t_relation''')
        cursor.execute('''create table t_relation 
            (twitter_user integer, foer integer,
            primary key(twitter_user, foer))''')
    except sqlite.InterfaceError:
        print "can't create talbe t_relation"

def get_connection():
    con = sqlite.connect(DATABASE,
        detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
    return con
