import sqlite3
import hashlib


class Database:
    def __init__(self, filename):
        # Connect to the database file
        self.datab = sqlite3.connect(filename)

        # Store the connection in the self.datab attribute
        self.cursor = self.datab.cursor()

    def add_user(self, username, password):
        # Check if the username exists in the table
        if not self.check_repeat(username):
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            self.cursor.execute("INSERT INTO users (id, name, password) VALUES (?,?,?)", (2,username, password_hash))
            print('user added')
        else:
            print('repeat detected')

    def check_repeat(self, username):
        # Query the database for an entry with the specified username
        result = self.datab.execute(
            "SELECT * FROM users WHERE name = ? AND EXISTS (SELECT 1 FROM users WHERE name = ?)",
            (username, username))

        # Check if any rows were returned
        if result.fetchone():
            return True
        else:
            return False

    def close_database(self):
        # Close the connection to the database
        self.datab.close()


# Create a new Database object
database = Database("usernames.db")

# Add a new user to the database
database.add_user('xander', 'hello!')

# Close the connection to the database
database.close_database()

