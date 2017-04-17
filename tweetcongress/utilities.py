import json, requests

class Tweet:
	"""Represents a Tweet. Stores the body of a Tweet, 
	and the username associated with the Tweet."""

	def __init__(self, username, body):
		self.username = username
		self.body = body

	def __repr__(self):
		return (self.username + self.body)

	def __str__(self):
		return (self.username + self.body)

class TwitterAPICommunicator:
	#"""Handles all communications with the Twitter API.
	#This includes both posting Tweets, and listening for and receiving Tweets."""

	@classmethod
	def tweet_to_zipcode(self, txt):
		tweet_bot_id = '@TweetAtCongress '
		id_len = len(tweet_bot_id)
		body = txt[id_len:]
		txt_len = len(body)

		if txt_len < 5:
			return False

		if txt_len >= 5:
			try:
				zipcode = int(body[0:5])
				return zipcode
			except ValueError:
				return False
		#"""Parses a raw tweet (JSON format) and returns the zip code requested by the user."""

	
class TweetCreator:

	@classmethod
	def make_zipcode_response(self, reps, username):
		print("Reps:", reps)
		n = len(reps)
		# body = "There are %d people who serve that zip code." % n
		body = "@"
		strs = []
		for i, rep in enumerate(reps):
			s = "%d: %s %s" % (i, rep.first, rep.last)
			strs.append(s)
		body += "".join(strs)
		return Tweet(username, body)

	@classmethod
	def daily_schedule(s):

		body = "On %s, %s(%s) is going to be held by %s" \
			%(s.date, s.name, s.type, s.house_of_congress)

	@classmethod
	def make_vote_result(v):

		if v.passed:
			result = "passed"
		else:
			result = "rejected"
		body = "On %s, with %d Congressmen voted yes and %d voted no, \
		the Bill %s is %s" \
		% (v.date, v.yes_votes, v.no_votes,v.bill_name, result)
	
		
class CongressAPICommunicator:
	"""Handles all communications with Congressional API.
	This includes fetching and parsing representatives by zip code, daily schedules, and live vote updates."""

	@classmethod
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
		

class Vote:
	def __init__(self, name, yes, no, passed, date):
		self.bill_name = name
		self.yes_votes = yes
		self.no_votes = no
		self.passed = passed
		self.date = date


class Event:
	def __init__(self, name, house_of_congress, date, typ):
		self.name = name
		self.house_of_congress = house_of_congress
		self.date = date
		self.type = typ
