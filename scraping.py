import requests
from HTMLParser import HTMLParser

url = "http://m.jpgushi.com/l/5000nian"

class get_urls(HTMLParser):
	def __init__(self):
		self.array = []
		self.tags = []
		HTMLParser.__init__(self)


	def handle_starttag(self, tag, attrs):
		dictionary = {}
		for x in attrs:
			dictionary[x[0]] = x[1]
		self.tags.append({'tag':tag, 'attrs':dictionary})

	def handle_data(self, data):
		if len(self.tags) > 2:
			if self.tags[-1]['tag'] == 'a' and self.tags[-2]['tag'] == 'li' and self.tags[-2]['attrs'].get('class', None) == 'jd':
				self.array.append(self.tags[-1]['attrs']['href'])

	def handle_endtag(self, tag):
		self.tags.pop()

	def getArray(self):
		return self.array

class get_chinese(HTMLParser):
	def __init__(self):
		self.outfile = open('data.txt', 'w')
		self.tags = []
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		dictionary = {}
		for x in attrs:
			dictionary[x[0]] = x[1]
		self.tags.append({'tag':tag, 'attrs':dictionary})

	def handle_data(self, data):
		if len(self.tags) > 2:
			if self.tags[-2]['attrs'].get('class', None) == 'acon' or self.tags[-3]['attrs'].get('class', None) == 'acon':
				self.outfile.write(data.encode('utf8'))

	def handle_endtag(self, tag):
		popped = self.tags.pop()
		# if popped['tag'] == 'p' and self.tags[-1]['attrs'].get('class', None) == 'acon':
		# 	self.outfile.write('\n')

def getResponse(url):

	headers = {
	    'cache-control': "no-cache",
	    'postman-token': "bc966681-64e3-4216-f6a3-6f4707725266"
	    }

	response = requests.request("GET", url, headers=headers)

	return response.text



scrapy = get_urls()
scrapy.feed(getResponse(url))
array_of_links = scrapy.getArray()
chinese = get_chinese()
for link in array_of_links:
	print link
	chinese.feed(getResponse(link))


