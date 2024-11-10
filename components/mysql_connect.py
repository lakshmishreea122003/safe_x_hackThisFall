import mysql.connector

class Database:
    def __init__(self):
        # Hardcoded database credentials and settings
        self.host = "localhost"
        self.user = "your_user"
        self.password = "your_password"
        self.database = "your_database"
        self.connection = None

    def connect(self):
        """Establish a connection to the database."""
        if self.connection is None or not self.connection.is_connected():
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

    def disconnect(self):
        """Close the database connection."""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()

    def save_tweet(self, tweet_data, is_harmful):
        """Save tweet information to the database."""
        self.connect()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO tweets (tweet_id, author_id, text, created_at, report)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        data = (
            tweet_data.id,
            tweet_data.author_id,
            tweet_data.text,
            tweet_data.created_at,
            is_harmful  # true if harmful content detected, else false
        )
        
        try:
            cursor.execute(query, data)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
        finally:
            cursor.close()
            self.disconnect()

# Example usage:
# db = Database()
# db.save_tweet(tweet_data, is_harmful=True)
