import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("messages.db", check_same_thread=False)


def init_db() -> None:
    """
    Creates a new SQLite database to store messages, if it doesn't exist already.

    Returns:
        None
    """

    conn.execute(
        """CREATE TABLE IF NOT EXISTS messages
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                role TEXT,
                message TEXT,
                timestamp TIMESTAMP)"""
    )


def insert_message(phone_number: str, role: str, message: str) -> None:
    """
    Inserts a new message into the database.

    Args:
        phone_number (str): The phone number of the sender or recipient.
        role (str): The role of the message sender, either "user" or "assistant".
        message (str): The text of the message.

    Returns:
        None
    """

    conn.execute(
        "INSERT INTO messages (phone_number, role, message, timestamp) VALUES (?, ?, ?, ?)",
        (phone_number, role, message, datetime.now()),
    )
    conn.commit()


def get_messages(phone_number: str, min: int = 30) -> list:
    """
    Retrieves all messages for a given phone number that occurred in the last `min` minutes.

    Args:
        phone_number (str): The phone number of the sender or recipient.
        min (int): The number of minutes before now to retrieve messages from. Default is 30.

    Returns:
        list: A list of tuples containing the message data.
    """

    thirty_minutes_ago = datetime.now() - timedelta(minutes=min)
    messages = conn.execute(
        "SELECT * FROM messages WHERE phone_number=? AND timestamp > ? ORDER BY timestamp ASC",
        (phone_number, thirty_minutes_ago),
    )
    return messages.fetchall()
