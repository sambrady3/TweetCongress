import unittest
from tweetcongress.utilities import CongressAPICommunicator, Representative

class CongressTestCase(unittest.TestCase):
	"""Tests for communicating with Congress API"""

	def test_zipcode_22033(self):
		"""Are the correct representatives returned for 22033?"""
		# communicator = CongressAPICommunicator()
		correct = [Representative('Barbara', 'Comstock', 'House'),
			Representative('Timothy', 'Kaine', 'Senate'),
			Representative('Gerald', 'Connolly', 'House'),
			Representative('Mark', 'Warner', 'Senate')]
		reps = CongressAPICommunicator.fetch_by_zipcode(22033)

		for i in range(len(reps)):
			self.assertEqual(correct[i].first, reps[i].first)
			self.assertEqual(correct[i].last, reps[i].last)
			self.assertEqual(correct[i].chamber, reps[i].chamber)

	def test_zipcode_99999(self):
		"""Is an empty list returned for an invalid zipcode?"""
		reps = CongressAPICommunicator.fetch_by_zipcode(99999)
		self.assertEqual(reps, [])
		
		def test_floor_updates(self):
		"""Could bills be fetched? Is every bill valid?"""
		global floor_updates
		floor_updates = CongressAPICommunicator.get_floor_updates()
		self.assertGreater(len(floor_updates), 0)
		for floor_update in floor_updates:
			self.assertTrue(validate(floor_update))

	def test_votes(self):
		"""Could votes be fetched? Is every vote valid?"""
		global votes
		votes = CongressAPICommunicator.get_votes()
		self.assertGreater(len(votes), 0)
		for vote in votes:
			self.assertTrue(validate(vote))

class CreatorTestCase(unittest.TestCase):
	"""Tests for Tweet creator functions"""

	def test_make_zipcode_response(self):
		"""Is Tweet made from reps valid?"""
		tweet = TweetCreator.make_zipcode_response(reps, "test")
		self.assertTrue(validate(tweet))

	def test_make_floor_update(self):
		"""Are Tweets made from floor_updates valid?"""
		for floor_update in floor_updates:
			tweet = TweetCreator.make_floor_update(floor_update)
			self.assertTrue(validate(tweet))

	def test_make_vote(self):
		"""Are Tweets made from votes valid?"""
		for vote in votes:
			tweet = TweetCreator.make_vote(vote)
			self.assertTrue(validate(tweet))


if __name__ == '__main__':
	unittest.main()
    
