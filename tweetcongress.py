class Tweet:
	"""Represents a Tweet. Stores the body of a Tweet, 
	and the username associated with the Tweet."""

	def __init__(self, username, body):
		self.username = username
		self.body = body

# class TwitterAPICommunicator:
	"""Handles all communications with the Twitter API.
	This includes both posting Tweets, and listening for and receiving Tweets."""

	# def parse_message(raw_tweet):
		"""Parses a raw tweet (JSON format) and returns the zip code requested by the user."""

class CongressAPICommunicator:
	"""Handles all communications with Congressional API.
	This includes fetching and parsing representatives by zip code, daily schedules, and live vote updates."""

	# def fetch_by_zipcode(zipcode):
		# TODO: This should return a list of Representative objects
