import json, requests

class Tweet:
	"""Represents a Tweet. Stores the body of a Tweet, 
	and the username associated with the Tweet."""

	def __init__(self, username, body):
		self.username = username
		self.body = body

# class TwitterAPICommunicator:
	#"""Handles all communications with the Twitter API.
	#This includes both posting Tweets, and listening for and receiving Tweets."""

	# def parse_message(raw_tweet):
		#"""Parses a raw tweet (JSON format) and returns the zip code requested by the user."""

class CongressAPICommunicator:
	"""Handles all communications with Congressional API.
	This includes fetching and parsing representatives by zip code, daily schedules, and live vote updates."""

	def fetch_by_zipcode(self, zipcode):
		reps = []

		# TODO: This should return a list of Representative objects
		url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip={}'.format(zipcode)

		r = requests.get(url)

		info = r.json()

		#Finding the number of representatives
		NumOfRep = info['count']

		# Getting every Rep fist & last names
		for i in range(NumOfRep):
			first = info['results'][i]['first_name']
			last = info['results'][i]['last_name']
			chamber = info['results'][i]['chamber']
			representative = Representive(first, last, chamber)

			reps.append(representative)
		return reps

class Representive:
	def __init__(self, first, last, chamber):
		self.first = first
		self.last = last
		self.chamber = chamber