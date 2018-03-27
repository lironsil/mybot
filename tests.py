
import unittest
from mybot import calc_average,is_number

class TestUM(unittest.TestCase):

	def setUp(self):
		pass
		
	def test_average(self):
		user='user1'
		number=4
		self.assertEqual(calc_average(number,user),4)
		number=8
		self.assertEqual(calc_average(number,user),6)

	def test_is_number(self):
		self.assertEqual(is_number(5),True)
		self.assertEqual(is_number("false"),False)
	
 
if __name__ == '__main__':
    unittest.main()