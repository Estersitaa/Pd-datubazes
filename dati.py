import sqlite3

# Datubāzes izveidošana un inicializācija
def init_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    # Reģistrētie lietotāji
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    # Ziņas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    connection.commit()
    connection.close()

# Pievienot lietotāju
def add_user(first_name, last_name, username):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (first_name, last_name, username) VALUES (?, ?, ?)',
                       (first_name, last_name, username))
        connection.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Šāds lietotājvārds jau eksistē")
    finally:
        connection.close()

# Pievienot ziņu
def add_message(user_id, message):
    if not message.strip():
        raise ValueError("Ziņojums nevar būt tukšs")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
    connection.commit()
    connection.close()

# Saņemt lietotāju sarakstu
def get_users():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('SELECT id, first_name, last_name, username FROM users ORDER BY username')
    users = cursor.fetchall()
    connection.close()
    return users

# Saņemt visas ziņas
def get_messages():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT users.first_name, users.last_name, messages.message, messages.timestamp 
        FROM messages 
        JOIN users ON messages.user_id = users.id 
        ORDER BY messages.timestamp DESC
    ''')
    messages = cursor.fetchall()
    connection.close()
    return messages

# Statistika
def get_user_statistics():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT users.first_name, users.last_name, COUNT(messages.id) as message_count
        FROM users
        LEFT JOIN messages ON messages.user_id = users.id
        GROUP BY users.id
    ''')
    stats = cursor.fetchall()
    connection.close()
    return stats
