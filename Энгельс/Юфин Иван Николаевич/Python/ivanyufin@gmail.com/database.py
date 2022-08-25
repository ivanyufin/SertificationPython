import sqlite3

db = sqlite3.connect("scores.sqlite")


def create_table():
    cur = db.cursor()
    cur.execute("""
    create table if not exists records(
        name text,
        score integer
    )""")
    cur.close()


def get_users_score():
    cur = db.cursor()
    cur.execute("""
    SELECT name, max(score) score FROM records
    GROUP by name
    ORDER by score DESC
    limit 5
    """)

    users_score = cur.fetchall()
    return users_score


def insert_user_score(user_name, score):
    cur = db.cursor()
    cur.execute("INSERT INTO records VALUES (?, ?)", (user_name, score))
    db.commit()
    cur.close()