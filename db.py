import sqlite3 as sq


class BotDB:
    def __init__(self, db_file):
        self.conn = sq.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT 'id' FROM 'users' WHERE 'user_id' = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, text):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT  INTO 'records' ('user_id', 'text') VALUES (?, ?)",
                            (self.get_user_id(user_id),
                             text))
        return self.conn.commit()

    def get_records(self, user_id, within="all"):
        """Получаем историю о доходах/расходах"""

        if (within == "day"):
            result = self.cursor.execute(
                "SELECT 'text' FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        elif (within == "week"):
            result = self.cursor.execute(
                "SELECT text FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        elif (within == "month"):
            result = self.cursor.execute(
                "SELECT text FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY 'date'",
                (self.get_user_id(user_id),))
        else:
            result = self.cursor.execute("SELECT * FROM 'records' WHERE 'user_id' = ? ORDER BY 'date'",
                                         (self.get_user_id(user_id),))

        return result.fetchall()


    def close(self):
        self.conn.close()
