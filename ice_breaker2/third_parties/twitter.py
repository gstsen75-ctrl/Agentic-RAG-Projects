import os
from dotenv import load_dotenv
import tweepy
import requests

'''twitter_client = tweepy.Client(
    bearer_token=os.environ["BEARER_TOKEN"],
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token=os.environ["ACCESS_TOKEN"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
)'''

def scrape_twitter_acc(username, num_tweets=5, mock: bool = False) :
    """Scrapes a Twitter user's original tweets, and returns them as a list of dicts.
    Each dict has three fields: "time_posted" (relative to now), "text", and "url" """

    tweet_list = []
    if mock:
        EDEN_TWITTER_GIST = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(EDEN_TWITTER_GIST, timeout=5).json()
        for tweet in tweets:
            tweet_dict = {}
            tweet_dict["text"]= tweet["text"]
            tweet_dict["url"]= f"https://twitter.com/{username}/status/{tweet['id']}"
            tweet_list.append(tweet_dict)
    return tweet_list
'''else:
        user_id= twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )
        for tweet in tweets:
            tweet_dict = {}
            tweet_dict["text"]= tweet["text"]
            tweet_dict["url"]= f"https://twitter.com/{username}/status/{tweet.id}"
            tweet_list.append(tweet_dict)'''


if __name__ == '__main__':
    tweets = scrape_twitter_acc(username="EdenEmarco177", mock=True)
    print(tweets)

