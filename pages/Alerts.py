import streamlit as st
from components.mysql_connect import Database

from streamlit_lottie import st_lottie
import requests

# Functions
# Function to load Lottie animations from a URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

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

st.markdown(
    """
    <style>
    .alert-title-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        background-color: #ffcccc; /* Light red background for alert */
        border-radius: 10px;
        border: 2px solid #ff0000; /* Bold red border */
    }

    .alert-title-text {
        font-family: Arial, sans-serif;
        font-size: 36px;
        font-weight: bold;
        color: #cc0000; /* Strong red color */
        text-align: center;
    }

    .alert-subtitle-text {
        font-size: 20px;
        color: #333333; /* Dark grey for subtitle */
        margin-top: 5px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# HTML structure for the alert title and subtitle
st.markdown(
    """
    <div class="alert-title-container">
        <div>
            <div class="alert-title-text">⚠️ Alert: Take Action Now ⚠️</div>
            <div class="alert-subtitle-text">Immediate attention required to address this alert</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# lotti
lottie_animation = load_lottie_url("https://lottie.host/d963154e-a4ec-4432-a09a-3151a112cd73/7cZkwMheql.json")
st_lottie(lottie_animation, height=300, width=300, key="animation")


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
