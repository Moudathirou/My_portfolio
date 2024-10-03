import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM admin_users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return True
    else:
        return False
