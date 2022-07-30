import sqlite3 as sq


try:
    conn = sq.connect('teleBot.db')
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTP 'users' ('user_id') VALUE (?), (1000,)")
    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

except sq.Error as error:
    print("Error", error)

finally:
    if (conn):
        conn.close()

