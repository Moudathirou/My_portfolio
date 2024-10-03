import sqlite3

def get_db_connection():
    conn = sqlite3.connect('portfolio.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, title TEXT, photo TEXT, github TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS experiences (id INTEGER PRIMARY KEY, title TEXT, company TEXT, start_date TEXT, end_date TEXT, description TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS skills (id INTEGER PRIMARY KEY, name TEXT)')
    conn.close()