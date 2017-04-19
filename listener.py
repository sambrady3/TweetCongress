import configparser
import json
import tweepy
from tweetcongress.utilities import CongressAPICommunicator, TwitterAPICommunicator, TweetCreator, Tweet

config = configparser.ConfigParser()
config.read('.config')
consumer_key = config['DEFAULT']['consumer_key']
consumer_secret = config['DEFAULT']['consumer_secret']
access_token = config['DEFAULT']['access_token']
access_token_secret = config['DEFAULT']['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class TweetCongressListener(tweepy.StreamListener):
    def on_data(self, data):
        tweet = json.loads(data.strip())
        tweetText = tweet.get('text')
        screenName = tweet.get('user',{}).get('screen_name')
        tweetId = tweet.get('id_str')

        print(tweetText)

        tweet_bot_id = '@TweetAtCongress '
        id_len = len(tweet_bot_id)
        body = tweetText[id_len:]
        txt_len = len(body)
        if body[:8] == "schedule":
            date = body[9:]
            bills = CongressAPICommunicator.schedule_for_day(date)
            schedule_response = TweetCreator.make_schedule_response(bills, screenName)
            TwitterAPICommunicator.send_tweet(schedule_response, api, tweetId)     
        else:    
            # parse the zipcode out
            zipcode = TwitterAPICommunicator.tweet_to_zipcode(tweetText)
            print("zipcode from 'tweet_to_zipcode': ", zipcode)

            if not zipcode:
                zipcode_response = Tweet(screenName, "We were unable to find a zipcode in your Tweet. Make sure you're sending us exactly 5 digits and nothing else.")
            else:
                reps = CongressAPICommunicator.fetch_by_zipcode(zipcode)
                if not reps:
                    zipcode_response = Tweet(screenName, "We were unable to find any representatives for that zipcode.")
                else:
                    zipcode_response = TweetCreator.make_zipcode_response(reps, screenName)

            TwitterAPICommunicator.send_tweet(zipcode_response, api, tweetId)         

    def on_error(self, status):
        print(status)

if __name__ == '__main__':    
    streamListener = TweetCongressListener()
    twitterStream = tweepy.Stream(auth, streamListener)
    twitterStream.filter(track=['@tweetatcongress'])
    twitterStream.userstream(_with='user', replies="all")

