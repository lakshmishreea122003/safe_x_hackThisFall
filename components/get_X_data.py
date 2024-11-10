import streamlit as st
import tweepy
from components.get_X_data import TwitterClient
import pickle
import os

# Initialize the Twitter client with your bearer token
twitter_client = TwitterClient()

# Function to get user profile from Twitter
def fetch_user_profile(username):
    user_profile = twitter_client.get_user_profile(username)
    if user_profile:
        return {
            "profile_image_url": user_profile.profile_image_url,
            "name": user_profile.name,
            "username": user_profile.username,
            "description": user_profile.description,
            "public_metrics": user_profile.public_metrics
        }
    else:
        st.error("Could not fetch user profile.")
        return None

# Function to fetch recent tweets
def fetch_recent_tweets(username):
    tweets = twitter_client.get_recent_tweets(username)
    return tweets

# Function to analyze and moderate tweet text (Harmful Content Detection)
def analyze_and_moderate_tweet(text):
    # Load pre-trained harmful content detection model and TF-IDF vectorizer
    try:
        with open("harmful_content_classifier.pkl", "rb") as model_file:
            model = pickle.load(model_file)
        with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        
        tweet_vectorized = vectorizer.transform([text])
        is_harmful = model.predict(tweet_vectorized)[0] == 1

        if is_harmful:
            return "This tweet contains harmful content."
        else:
            return text  # Return the tweet as is if not harmful

    except Exception as e:
        st.error("Error in content analysis.")
        print("An error occurred during harmful content analysis:", e)
        return text

# Profile Section
username = "LakshmiShreeA1"  # Replace with dynamic username input if required
user_profile = fetch_user_profile(username)

if user_profile:
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
        st.write(f"**Posted on:** {tweet.created_at.strftime('%Y-%m-%d %H:%M')}")
        moderated_text = analyze_and_moderate_tweet(tweet.text)
        st.write(moderated_text)

        # Fetch replies if needed (handle replies separately or as comments)
        with st.expander("View Replies"):
            replies = twitter_client.get_replies(tweet.id)
            if replies:
                for reply in replies:
                    moderated_reply = analyze_and_moderate_tweet(reply.text)
                    st.write(f"**Reply by @{reply.author_id} on {reply.created_at.strftime('%Y-%m-%d %H:%M')}:** {moderated_reply}")
            else:
                st.write("No replies found.")
        
        st.write("----")
else:
    st.write("No recent tweets found.")
