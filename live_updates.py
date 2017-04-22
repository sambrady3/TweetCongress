import arrow
import configparser
import time
import tweepy
from tweetcongress.utilities import CongressAPICommunicator, TwitterAPICommunicator, TweetCreator, Tweet, FloorUpdate

config = configparser.ConfigParser()
config.read('.config')
consumer_key = config['DEFAULT']['consumer_key']
consumer_secret = config['DEFAULT']['consumer_secret']
access_token = config['DEFAULT']['access_token']
access_token_secret = config['DEFAULT']['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def main():
	most_recent_update = arrow.utcnow()
	most_recent_vote = arrow.utcnow()
	while True:
		print("Most recent update: {}".format(most_recent_update.format("YYYY/MM/DD HH:mm")))
		print("Most recent vote:   {}".format(most_recent_vote.format("YYYY/MM/DD HH:mm")))
		print("Current time:       {}".format(arrow.utcnow().format("YYYY/MM/DD HH:mm")))
		new_updates = get_new_updates(most_recent_update)
		new_votes = get_new_votes(most_recent_vote)
		for upd in new_updates:
			if upd.timestamp > most_recent_update:
				most_recent_update = upd.timestamp
			tweet = TweetCreator.make_floor_update(upd)
			TwitterAPICommunicator.send_tweet(tweet, api, None)

		for vote in new_votes:
			if vote.timestamp > most_recent_vote:
				most_recent_vote = vote.timestamp
			tweet = TweetCreator.make_vote(vote)
			TwitterAPICommunicator.send_tweet(tweet, api, None)
		time.sleep(180)


def get_new_updates(most_recent):
	floor_updates = CongressAPICommunicator.get_floor_updates()
	new_updates = []
	for upd in floor_updates:
		if upd.timestamp > most_recent:
			new_updates.append(upd)

	return new_updates

def get_new_votes(most_recent):
	votes = CongressAPICommunicator.get_votes()
	new_votes = []
	for vote in votes:
		if vote.timestamp > most_recent:
			new_votes.append(vote)

	return new_votes



if __name__ == '__main__':
	main()