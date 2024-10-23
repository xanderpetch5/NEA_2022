import sqlite3
import hashlib

class Database:
    def __init__(self, filename):
        self.datab = sqlite3.connect(filename)

        self.cursor = self.datab.cursor()

    def add_user(self, username, password):
        if not self.check_repeat(username):
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            self.cursor.execute("SELECT MAX(id) FROM users")
            max_id = self.cursor.fetchone()[0]

            try:
                self.cursor.execute("INSERT INTO users (id, name, password, user_history) VALUES (?,?,?,?)", (max_id + 1, username, password_hash,''))
            except:
                self.cursor.execute("INSERT INTO users (id, name, password, user_history) VALUES (?,?,?,?)",
                                    (1, username, password_hash,''))
            self.datab.commit()
            print('user added')
        else:
            print('repeat detected')

    def check_repeat(self, username):
        result = self.cursor.execute("SELECT 1 FROM users WHERE name = ?", (username,))

        if result.fetchone():
            return True
        else:
            return False

    def check_credentials(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        result = self.cursor.execute(
            "SELECT * FROM users WHERE name = ? AND password = ?",
            (username, password_hash))

        if result.fetchone():
            return True
        else:
            return False

    def delete_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        result = self.datab.execute(
            "SELECT * FROM users WHERE name = ? AND password = ?",
            (username, password_hash))

        user = result.fetchone()
        if user:
            user_id = user[0]
            print(user_id)
            self.cursor.execute("DELETE FROM users WHERE name=? AND password=?", (username, password_hash))

            self.datab.execute("UPDATE users SET id = id - 1 WHERE id > ?", (user_id,))
            self.datab.commit()
            print(f'User {username} deleted')
        else:
            print('User not found')

    def fetch_history(self, username):
        self.cursor.execute('SELECT user_history FROM users WHERE name=?', (username,))

        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def update_history(self, username, new_history):
        self.cursor.execute('UPDATE users SET user_history=? WHERE name=?', (new_history, username))

        self.datab.commit()

    def change_password(self, username, new_password):
        # Hash the new password
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        self.cursor.execute('UPDATE users SET password=? WHERE name=?', (new_password_hash, username))

        self.datab.commit()

    def close_database(self):
        self.datab.close()

