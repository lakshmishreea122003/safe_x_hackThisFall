import streamlit as st
from components.mysql_connect import Database

# Initialize database connection
db = Database()

# Function to fetch tweets from the database
def fetch_tweets_from_db():
    db.connect()  # Ensure connection to the database
    cursor = db.connection.cursor(dictionary=True)
    cursor.execute("SELECT tweet_id, author_id, text, created_at, report FROM tweets WHERE report = 0")
    tweets = cursor.fetchall()
    cursor.close()
    db.disconnect()
    return tweets

# Function to update the report status in the database
def update_report_status(tweet_id):
    db.connect()
    cursor = db.connection.cursor()
    query = "UPDATE tweets SET report = %s WHERE tweet_id = %s"
    cursor.execute(query, (True, tweet_id))  # Set report to True (1) for reported tweets
    db.connection.commit()
    cursor.close()
    db.disconnect()

# Display the Alerts page in Streamlit
st.title("Alerts: Take Action Now")
st.write("Review flagged tweets and report if necessary.")

# Fetch tweets from the database
tweets = fetch_tweets_from_db()

# Display each tweet with a report button
for index, tweet in enumerate(tweets, start=1):
    with st.container():
        st.write(f"**{index}. @{tweet['author_id']}**")
        st.write(tweet["text"])
        st.caption(f"Date: {tweet['created_at']}")

        # Show 'Reported' if already reported, else show 'Report' button
        if tweet["report"]:
            st.info("Status: Reported")
        else:
            if st.button(f"Report Tweet ID: {tweet['tweet_id']}", key=tweet["tweet_id"]):
                update_report_status(tweet["tweet_id"])
                st.success("Status: Reported")

        st.write("---")  # Separator between tweets
