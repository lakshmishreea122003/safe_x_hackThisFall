import streamlit as st
import google.generativeai as genai
import os
import tweepy  # Assuming you're using Tweepy to interact with Twitter API

# Replace with your actual API key from Google AI Studio
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Twitter API Authentication
auth = tweepy.OAuth1UserHandler(consumer_key=TWITTER_API_KEY,
                                consumer_secret=TWITTER_API_SECRET_KEY,
                                access_token=TWITTER_ACCESS_TOKEN,
                                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Choose appropriate Gemini model for text moderation
model_name = "gemini-1.5-flash"  # Replace with the desired model
model = genai.GenerativeModel(model_name)

# Function to fetch user profile from Twitter
def fetch_user_profile(username):
    user = api.get_user(screen_name=username)
    return {
        "profile_image_url": user.profile_image_url,
        "name": user.name,
        "username": user.screen_name,
        "description": user.description,
        "public_metrics": {
            "followers_count": user.followers_count,
            "following_count": user.friends_count,
            "tweet_count": user.statuses_count
        }
    }

# Function to fetch recent tweets from Twitter
def fetch_recent_tweets(username):
    tweets = api.user_timeline(screen_name=username, count=5, tweet_mode="extended")
    recent_tweets = []
    for tweet in tweets:
        tweet_data = {
            "id": tweet.id,
            "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M"),
            "text": tweet.full_text,
            "replies": []  # Assuming no replies data is available from the API directly, needs workaround
        }
        recent_tweets.append(tweet_data)
    return recent_tweets

# Moderation function with Gemini
def moderate_text(text, safety_level):
    prompt = f"Rewrite the following text in a safer manner, suitable for all audiences: '{text}'. Safety level: {safety_level}/10. If the safety level is 0, return the text as it is. Otherwise, modify the text to make it safer."
    response = model.generate_text(prompt=prompt)
    return response.text[0]

# Profile Section
username = "LakshmiShreeA1"  # Replace with dynamic username input if required
user_profile = fetch_user_profile(username)

st.markdown(
    f"""
    <style>
    .profile-container {{
        display: flex;
        align-items: center;
        padding: 20px;
    }}
    .profile-pic {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-right: 20px;
        object-fit: cover;
    }}
    .profile-details {{
        font-family: 'Courier New', Courier, monospace;
    }}
    .profile-name {{
        font-size: 28px;
        font-weight: bold;
        color: #1DA1F2; /* Twitter's brand blue */
    }}
    .profile-username {{
        font-size: 20px;
        color: #657786; /* Twitter's grey for usernames */
    }}
    </style>
    
    <div class="profile-container">
        <img class="profile-pic" src="{user_profile['profile_image_url']}">
        <div class="profile-details">
            <div class="profile-name">{user_profile['name']}</div>
            <div class="profile-username">@{user_profile['username']}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Safety slider
safety_level = st.slider("Set Safety Level (0 - Normal, 10 - Safe)", 0, 10, 5)
st.write(f"**Safety Level Set:** {safety_level}")

# Divider
st.write("---")

# Fetch recent tweets
recent_tweets = fetch_recent_tweets(username)

# Tweets Section
st.write("### Recent Tweets")

if recent_tweets:
    for tweet in recent_tweets:
        st.write(f"**Posted on:** {tweet['created_at']}")
        st.write(tweet["text"])

        # For replies (if available)
        with st.expander("View Replies"):
            replies = tweet["replies"]
            if replies:
                for idx, reply in enumerate(replies, start=1):
                    moderated_reply = moderate_text(reply["text"], safety_level)
                    st.markdown(f"<p><b>{idx}. Reply by User ID {reply['author_id']} on {reply['created_at']}:</b> {moderated_reply}</p>", unsafe_allow_html=True)
            else:
                st.write("No replies found.")
        
        st.write("----")
else:
    st.write("No recent tweets found.")
