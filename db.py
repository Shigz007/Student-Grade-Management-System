import sqlite3
from config import DATABASE, SCHOOL_DATABASE


def get_db():
    import os as _os
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if _os.path.exists(SCHOOL_DATABASE):
        conn.execute("ATTACH DATABASE ? AS school", (SCHOOL_DATABASE,))
    return conn


def init_db():
    # Main database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    # School database — separate connection so tables go into school.db
    conn = sqlite3.connect(SCHOOL_DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    with open('school_schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def query(sql, args=(), one=False):
    conn = get_db()
    cur = conn.execute(sql, args)
    rows = cur.fetchall()
    conn.close()
    if rows and one:
        return dict(rows[0])
    return [dict(r) for r in rows]


def execute(sql, args=()):
    conn = get_db()
    cur = conn.execute(sql, args)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id
