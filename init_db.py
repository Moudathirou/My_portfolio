import sqlite3

def init_db():
    conn = sqlite3.connect('admin.db')
    cursor = conn.cursor()

    # Création de la table des utilisateurs admins
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Insertion d'un utilisateur admin
    cursor.execute('''
    INSERT INTO admin_users (username, password)
    VALUES (?, ?)
    ''', ('Mouda', 'Moud1234569'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
