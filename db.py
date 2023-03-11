import sqlite3

from datetime import datetime, timedelta

conn = sqlite3.connect("messages.db", check_same_thread=False)


# Connect to the database
def init_db() -> None:
    # Create a table to store messages
    conn.execute(
        """CREATE TABLE IF NOT EXISTS messages
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                role TEXT,
                message TEXT,
                timestamp TIMESTAMP)"""
    )


# Function to insert new message into database
def insert_message(phone_number, role, message):
    conn.execute(
        "INSERT INTO messages (phone_number, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (phone_number, role, message, datetime.now()),
    )
    conn.commit()


# Function to retrieve all messages for a given phone number that occurred in the last 30 minutes
def get_messages(phone_number, min: int = 30):
    thirty_minutes_ago = datetime.now() - timedelta(minutes=min)
    messages = conn.execute(
        "SELECT * FROM messages WHERE phone_number=? AND timestamp > ? ORDER BY timestamp ASC",
        (phone_number, thirty_minutes_ago),
    )
    return messages.fetchall()
