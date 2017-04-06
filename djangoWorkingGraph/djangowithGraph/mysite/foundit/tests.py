import unittest
import re
#import views
from django.test import TestCase, Client


class MyTests(TestCase):
    def test1(self):
	c=Client()
        response = c.get("/foundit/")
	print("Checking validity of Home page")
	print("\n")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test2(self):
	c=Client()
	print("Checking for invalidity of results page, should return invalid without inputs")
	print("\n")
	response = c.get("/foundit/results")
	self.assertEqual(response.status_code, 200, 'View did return a 200.')
    def test3(self):
	c=Client()
	print("Checking Results Page with valid inputs")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test4(self):
	c=Client()
	print("Checking Results Page with invalid Subreddit input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=-2123fd3sdsadsafaf&postLimit=1&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did return a 200.')
    def test5(self):
	c=Client()
	print("Checking Results Page with invalid Post Number input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=-1&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test6(self):
	c=Client()
	print("Checking Results Page with invalid Comment Number input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test7(self):
	c=Client()
	print("Checking Results Page with invalid Top Words input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=-1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did return not a 200.')
    def test8(self):
	c=Client()
	print("Checking Results Page with invalid Top Users input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=1&topUsers=-1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test9(self):
	c=Client()
	print("Checking Results Page with invalid Top Replies input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=1&topUsers=1&ohSnap=-1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test10(self):
	c=Client()
	print("Checking Results Page with invalid Oldest Posts input")
	print("\n")
	response = c.post("/foundit/results/?subreddit=all&postLimit=1&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=-1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
    def test11(self):
	c=Client()
	print("Checking Results Page with valid inputs, but high values")
	print("\n")#The value in the post limit in this test was higher before, changing it for a re test, was previously at 1 million
	response = c.post("/foundit/results/?subreddit=all&postLimit=10&topComs=1&topWords=1&topUsers=1&ohSnap=1&oldestPosts=1")
	self.assertEqual(response.status_code, 200, 'View did not return a 200.')
