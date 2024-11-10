import streamlit as st
from streamlit_lottie import st_lottie
import requests

from components.get_X_data import TwitterClient

# Function to load Lottie animations from a URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()



# Initialize Twitter client and database
twitter_client = TwitterClient()
username = "target_username"  # Replace with the actual username
tweet_id = "target_tweet_id"  # Replace with the tweet ID to fetch replies
# Fetch recent tweets
recent_tweets = twitter_client.get_recent_tweets(username=username, max_results=10)
# Fetch mentioned tweets
mentioned_tweets = twitter_client.get_mentioned_tweets(username=username, max_results=10)
# Fetch replies to a specific tweet
replies = twitter_client.get_replies(tweet_id=tweet_id, max_results=10)
# Combine all tweets into a single list for analysis
all_tweets = recent_tweets + mentioned_tweets + replies
# Analyze each tweet and store harmful ones in MySQL
twitter_client.analyze_and_store_tweets(all_tweets)

# title
import streamlit as st

# Neon cyan blurred title for Streamlit (suitable for dark theme)
st.markdown(
    """
    <style>
    .neon-title {
        font-size: 80px;
        font-weight: bold;
        color: white;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 
            0 0 5px #00FFFF, 
            0 0 10px #00FFFF, 
            0 0 20px #00FFFF, 
            0 0 40px #00FFFF, 
            0 0 80px #00FFFF, 
            0 0 100px #00FFFF;
        margin-top: 50px;
    }

    .neon-tagline {
        font-size: 24px;
        color: #00FFFF;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 20px;
        font-weight: normal;
    }

    .blur-background {
        background: rgba(0, 0, 0, 0.6); /* Dark semi-transparent background */
        backdrop-filter: blur(10px); /* Blurred background */
        padding: 20px;
        border-radius: 15px;
        display: inline-block;
    }
    </style>
    
    <div class="blur-background">
        <div class="neon-title">SafeX</div>
        <div class="neon-tagline">AI-powered safety for women on social media.</div>
    </div>
    """,
    unsafe_allow_html=True
)


# description
st.write("Welcome to Safe_X – a social media platform designed to empower women by creating a safer online space. Using AI and machine learning, Safe_X detects harmful content, moderates negative language, and provides real-time support through an AI-powered chatbot. Stay connected with peace of mind, knowing your safety and well-being are our top priority.")

# Load the Lottie animation (replace URL with your chosen Lottie animation URL)
lottie_animation = load_lottie_url("https://lottie.host/ab48bede-586c-4c32-aad9-1255dbbeb6f2/RUVyzWwGts.json")

# Display the Lottie animation in Streamlit
st_lottie(lottie_animation, height=300, width=300, key="animation")
