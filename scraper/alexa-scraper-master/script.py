#!/usr/bin/env python
# ========================== Imports ========================== #
import sys
import time
from math import ceil

# To Maintain backporing to Python 2.7.12 and Suppoert for 3 libs together
is_python3 = sys.version_info.major == 3
if is_python3:
	from urllib.request import urlopen, Request, HTTPError
	from html.parser import HTMLParser
else:
	from urllib2 import urlopen, Request, HTTPError
	from HTMLParser import HTMLParser

# ========================== HTML Parser Class/Functions ========================== #

class htmlparser(HTMLParser):
	"""
	HTML Parser to parse scraped data from website
	"""

	def __init__ (self, n=50):
		"""
		Constructor
		"""
		HTMLParser.__init__(self)
		self.start = None
		self.head = None
		self.links = []
		self.count = 0
		self.n = n

	def handle_starttag(self, tag, attribs):
		"""
		Method to take action on starting tag
		"""
		if (tag == 'li' and self.count < self.n):
			for name, value in attribs:
				if (name == 'class' and value == 'site-listing'):
					self.head = True
					
		if (tag == 'a'):
			for name, value in attribs:
				if (name == 'href' and ('siteinfo' in value)):
					self.start = True

	def handle_data(self, data):
		"""
		Method to take action on data received from HTML tags
		"""
		if (self.start == True and self.head == True):
			self.count += 1
			self.links.append(data)
			
	def handle_endtag(self, data):
		"""
		Method to take action on ending tag
		"""
		if (self.start == True and data == 'a'):
			self.start = False
		if (self.head == True and data == 'li'):
			self.head = False

# ========================== Helper Functions ========================== #

def calc_number_of_pages(n):
	"""
	Calculate the number of pages need to be scraped
	based on the number of links required
	"""
	one_page_size = 25.0
	return int(ceil(n/one_page_size))

def print_top(list_of_sites):
	"""
	Print top links from the final list
	"""
	for site in range(len(list_of_sites)):
		print(str(site + 1) + ". " + list_of_sites[site])

# ========================== Main Calling Functions ========================== #

def scrape(n=50, sub_dir="topsites", local="global", sub_local=""):
	"""
	Scrape the given number of pages from alexa website
	"""
	n = int(n)
	if (n > 500): 
		print("Alexa Top 500 has at most 500 Links.")
		n = 500

	# If local is category, sub_local needs to be specially handled
	if (local == "category"):
		new_sub_local = ""

		# Converting each letter after / to be uppercase, otherwise link will result in no response
		for each_sub in range(len(sub_local)):
			if (sub_local[each_sub - 1] == '/' or each_sub == 0):
				new_sub_local += sub_local[each_sub].upper()
			else: new_sub_local += sub_local[each_sub]

		sub_local = "Top/" + new_sub_local

	# Additional Headers to make it more human.
	request_headers = {
					"Accept-Language": "en-US,en;q=0.5",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/50.0",
					"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
					"Connection": "keep-alive" }

	# To calculate time for programme to run
	start = time.clock()

	# Get the number of pages we need to scrape
	num_of_pages = calc_number_of_pages(n)
	final_list = []

	for page_num in range(num_of_pages):

		# Generate the complete url based on input
		full_url = "http://www.alexa.com/" + sub_dir + "/" + local + ";" + str(page_num) + "/" + str(sub_local)

		# Collect page data for current page
		page = ""

		# Try Making a request
		try:
			request = Request(full_url, headers=request_headers)
		except e:
			print(e.reason)

		response = urlopen(request)
		for line in response:
			line = line.decode('utf-8','ignore')
			page += line
		response.close()
		# Create a new parser for n links
		parser = htmlparser(n=n)

		# Reduce total by 25 links, since there are 25 links on each page
		n -= 25

		# Parse the collected page feed
		parser.feed(page)

		# Append the links to the final list
		final_list += parser.links

	# Print them in a readable way
	print_top(final_list)

	# print(str(time.clock() - start))
	return final_list


# ========================== Boiler Plate Functions ========================== #
def main():
	"""
	Main and argument acceptance
	"""
	
	# In case if user does not provide a parameter, 50 is defaulted
	if (len(sys.argv) == 1):
		scrape()

	# When user provides n
	elif (len(sys.argv) == 2):
		try:
			num = sys.argv[1]
			num = int(num)
			scrape(n=num)
		except ValueError:
			print("Not an Integer")

	# When user provides by local and sub local
	elif (len(sys.argv) == 4 and (sys.argv[2] == 'category' or sys.argv[2] == 'countries')):
		num, local, sub_local = sys.argv[1:]
		try:
			num = int(sys.argv[1])
		except ValueError:
			print("Not an Integer")
		scrape(n=num, local=local, sub_local=sub_local)

	# When user gives an unknown format of unknown, show them option
	else:
		print("Maybe you missed a parameter\n \
			List of Valid Command Formats: \n \
			1.) python script-name.py \n \
			2.) python script-name.py number-of-links \n \
			3.) python script-name.py number-of-links countries country-code \n \
			4.) python script-name.py number-of-links category sub-category1/sub-category2/sub-categoryn/")

if __name__ == "__main__":
	main()