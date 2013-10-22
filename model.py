import sqlite3, datetime

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    connect_to_db()
    query = """select id, username, password from users where username = ? and password = ?"""
    DB.execute(query, (username, password))
    row = DB.fetchone()
    if row == None:
        return None
    elif username == row[1] and password == row[2]:
        return row[0]

def get_username(user_id):
    connect_to_db()
    query = """SELECT username from users where id = ? """
    DB.execute(query, (user_id,))   
    row = DB.fetchone()
    return row

def get_user_id(username):
    connect_to_db()
    query = """SELECT id from users where username = ? """
    DB.execute(query, (username,))
    row = DB.fetchone()
    return row

def get_wall_posts(user_id):
    print type(user_id)
    connect_to_db()
    query = """select content, username, created_at from wall_posts inner join users on users.id = author_id where author_id = ?"""
    DB.execute(query, (user_id,))
    row = DB.fetchall()
    return row

def make_wall_post(username, user_id, content):
    connect_to_db()
    query = """INSERT into wall_posts (owner_id, author_id, created_at, content) values(?, ?, ?, ?)"""
    DATE = datetime.datetime.now()
    DATE = DATE.strftime("%d-%b-%Y")
    DB.execute(query, (username, user_id, DATE, content))
    CONN.commit()

    
    
    # if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
    #     return ADMIN_USER
    # else:
    #     return None
