import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_post(self, url_post, sent, not_sent, type):
        with self.connection:
            return self.cursor.execute("INSERT INTO `added_posts` (`url_post`, `sent`, `not_sent`, `type`) VALUES (?, ?, ?, ?)", (url_post, sent, not_sent, type,))

    def viewing_post(self):
        with self.connection:
            return self.cursor.execute("SELECT `url_post`, `sent`, `not_sent`, `type` FROM `added_posts`").fetchall()
