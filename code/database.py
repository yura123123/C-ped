import sqlite3

from os import path, makedirs


class DB_Exception(Exception):
    pass


# The path to directory this code is ran in.
CUR_PATH = path.dirname(path.abspath(__file__))

database_path = path.join(CUR_PATH, "../database")

# Users database filename.
users_db_fn = "users.db"

# Users database filepath.
users_db_fp = path.join(database_path, users_db_fn)


def init_user_database():
    # Create file, and dirs, if those do not exist.
    makedirs(database_path, exist_ok=True)
    with open(users_db_fp, "w+"):
        pass

    user_db = sqlite3.connect(users_db_fp)
    user_db_cursor = user_db.cursor()
    user_db_cursor.execute(
        """
        CREATE TABLE users
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        super_secret TEXT,
        secret_salt TEXT,
        name TEXT,
        email TEXT UNIQUE,
        pfp TEXT,
        google_id TEXT UNIQUE,
        permissions INTEGER)
        """
    )


def init_databases():
    init_user_database()


def setup():
    init_databases()


if __name__ == "__main__":
    setup()
elif not path.exists(users_db_fp):
    init_user_database()

user_db = sqlite3.connect(users_db_fp)
# A cursor for work with user database.
user_db_cursor = user_db.cursor()
