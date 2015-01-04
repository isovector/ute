import sqlite3
from os.path import expanduser

_conn = sqlite3.connect("%s/.ute.db" % expanduser("~"))
c = _conn.cursor()


def create(drop = False):
    if drop:
        c.execute("DROP TABLE interval")
    c.execute("""
    CREATE TABLE interval (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        type TEXT NOT NULL,
        desc TEXT NOT NULL,
        open INTEGER NOT NULL,
        close INTEGER
    )
    """)
    commit()

def commit():
    _conn.commit()

def execute(sql, args = None):
    c.execute(sql, args)

def query(sql, args = None):
    c.execute(sql, args)
    return c.fetchall()

def query1(sql, args = None):
    c.execute(sql, args)
    return c.fetchone()

def insert(sql, args = None):
    c.execute(sql, args)
    return c.lastrowid
