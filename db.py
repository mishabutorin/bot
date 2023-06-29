import sqlite3

__connection = None


def connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('db.db') as conn:
            result = func(*args, conn=conn, **kwargs)
        return result

    return inner


@connection
def init_db(conn, force: bool = False):
    cur = conn.cursor()

    if force:
        cur.execute('DROP TABLE IF EXISTS user_message')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER,
            user_category    TEXT,
            user_branch      TEXT,
            user_object      TEXT,
            firstname_lastname_info TEXT,
            user_number_phone_or_email TEXT,
            user_question        TEXT
        )
    ''')
    conn.commit()


@connection
def add_message(conn, user_id: int, user_category: str, user_branch: str, user_object: str,
                firstname_lastname_info: str, user_number_phone_or_email: str, user_question: str):
    cur = conn.cursor()
    cur.execute("INSERT INTO user_message  "
                "(user_id, user_category, user_branch, user_object, firstname_lastname_info, "
                "user_number_phone_or_email, user_question) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, user_category, user_branch,
                 user_object, firstname_lastname_info,
                 user_number_phone_or_email, user_question))
    conn.commit()


if __name__ == '__main__':
    init_db()
