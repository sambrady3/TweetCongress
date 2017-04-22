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

if __name__ == '__main__':
	unittest.main()
    