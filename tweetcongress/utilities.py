import json, requests, arrow

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

	@staticmethod
	def tweet_to_zipcode(txt):
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

	@staticmethod
	def send_tweet(tweet, connection, tweetId):
		body = tweet.body
		if tweet.username:
			text = '@' + tweet.username + " " + body
		else:
			text = body
		connection.update_status(status=text, in_reply_to_status_id=tweetId) 

	
class TweetCreator:

	@staticmethod
	def make_zipcode_response(reps, username):
		print("Reps:", reps)
		n = len(reps)
		body = "\n"
		strs = []
		for i, rep in enumerate(reps):
			if rep.chamber == "House":
				s = "%s %s (%s) District %d\n" % (rep.first, rep.last, rep.chamber[0], rep.district)
			else:
 				s = "%s %s (%s)\n" % (rep.first, rep.last, rep.chamber[0])
			strs.append(s)
		body += "".join(strs)
		return Tweet(username, body)

	@staticmethod
	def make_schedule_response(bills, username):
		date = bills[0].date
		tweets = []

		body = "Schedule for {}:\n".format(date)

		for bill in bills:
			body += bill.id + " " + bill.url + "\n"

		return Tweet(username, body)

	@staticmethod
	def make_floor_update(update):
		body = u"At {} in the {}\n{}".format(update.timestamp.format('HH:mm'), update.chamber, update.update) 

		if len(body) > 140:
			body = body[:139] + u'\u2026'

		print(len(body))

		return Tweet("", body)

	@staticmethod
	def make_vote(vote):
		body = u"{} VOTE RESULT\n{}: {}".format(vote.chamber.upper(), vote.question, vote.result) 

		if len(body) > 140:
			body = body[:139] + u'\u2026'

		print(len(body))

		return Tweet("", body)
	
		
class CongressAPICommunicator:
	"""Handles all communications with Congressional API.
	This includes fetching and parsing representatives by zip code, daily schedules, and live vote updates."""

	@staticmethod
	def fetch_by_zipcode(zipcode):
		reps = []

		url = 'https://congress.api.sunlightfoundation.com/legislators/locate?zip={}'.format(zipcode)
		r = requests.get(url)
		info = r.json()

		#Finding the number of representatives
		numOfRep = info['count']

		# Getting every Rep first & last names
		for i in range(numOfRep):
			first = info['results'][i]['first_name']
			last = info['results'][i]['last_name']
			chamber = info['results'][i]['chamber']
			chamber = chamber[0].upper() + chamber[1:]
			representative = Representative(first, last, chamber)

			reps.append(representative)
		return reps

	@staticmethod
	def schedule_for_day(date):
		# TODO: deal with formatting of date
		# needs to be YYYY-MM-DD

		# need to deal with formatting of tweet. Links with bill_id?

		bills = []

		url = 'https://congress.api.sunlightfoundation.com/upcoming_bills?legislative_day={}'.format(date)

		r = requests.get(url)
		info = r.json()

		num_of_bills = info['count']
		# num_of_bills = 3

		for i in range(num_of_bills):
			bill = info['results'][i]
			bill_id = bill['bill_id']
			chamber = bill['chamber']
			chamber = chamber[0].upper() + chamber[1:]
			bill_url = bill['bill_url']

			bills.append(Bill(bill_id, chamber, date, bill_url))

		return bills

	@staticmethod
	def get_floor_updates():
		URL = """https://congress.api.sunlightfoundation.com/floor_updates?order=timestamp"""
		r = requests.get(URL)
		info = r.json()
		# num_of_updates = info['count']
		num_of_updates = 20
		floor_updates = []

		for i in range(num_of_updates):
			raw_update = info['results'][i]
			update = raw_update['update']
			timestamp = arrow.get(raw_update['timestamp'])
			date = raw_update['legislative_day']
			chamber = raw_update['chamber']
			chamber = chamber[0].upper() + chamber[1:]
			floor_updates.append(FloorUpdate(update, timestamp, date, chamber))

		return sorted(floor_updates, key=lambda upd: upd.timestamp)

	@staticmethod
	def get_votes():
		URL = """https://congress.api.sunlightfoundation.com/votes?order=voted_at"""
		r = requests.get(URL)
		info = r.json()
		# num_of_updates = info['count']
		num_of_votes = 20 # number that fits on one page. only check most current page
		votes = []

		for i in range(num_of_votes):
			vote = info['results'][i]
			roll_id = vote['roll_id']
			chamber = vote['chamber']
			timestamp = arrow.get(vote['voted_at'])
			question = vote['question']
			result = vote['result']
			votes.append(Vote(roll_id, chamber, timestamp, question, result))

		return sorted(votes, key=lambda upd: upd.timestamp)


class Representative:
	def __init__(self, first, last, chamber):
		self.first = first
		self.last = last
		self.chamber = chamber
		

class Vote:
	def __init__(self, roll_id, chamber, timestamp, question, result):
		self.roll_id = roll_id
		self.chamber = chamber
		self.timestamp = timestamp
		self.question = question
		self.result = result


class FloorUpdate:
	def __init__(self, update, timestamp, date, chamber):
		self.update = update
		self.timestamp = timestamp
		self.date = date
		self.chamber = chamber


class Bill:
	def __init__(self, bill_id, house_of_congress, date, url):
		self.id = bill_id
		self.house_of_congress = house_of_congress
		self.date = date
		self.url = url
