#!/usr/bin/env jython
# -*- coding: utf-8 -*-

import requests, requests.utils, pickle
from os.path import join, isfile
import re

class GoogleSearcher:
	def __init__(self):
		self.cookie_path = join("/tmp", ".google-cookie")
		self.session = None
		self.load_session()

	def save_session(self):
		with open(self.cookie_path, 'w') as f:
			pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

	def load_session(self):
		try:
			print "Load cookie from %s" % self.cookie_path
			with open(self.cookie_path) as f:
				cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
				#print "Cookie: %s" % cookies
				self.session = requests.Session()
				self.session.cookies = cookies
		except:
			print "Created a cookie. Issue the request again"
			self.session = requests.Session()
			
	def request(self, query):
		query = {"query": query.replace(" ", "+")}
		url = "http://www.google.com/search?hl=en&q=%(query)s&btnG=Google+Search&inurl=https" % (query)
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36', 'accept-encoding': 'gzip;q=0,deflate,sdch'}

		#headers = {'User-Agent':'Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
		#headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0'}
		print 'Query: ', query
		print 'URL: ', url
		r = self.session.get(url, headers=headers)
		self.save_session()
		return r.text.encode("utf-8")

	def stackoverflow_questions(self, query):
		#query = "stackoverflow java %s" % query
		html = self.request(query)
		print html
		for i in re.findall(r'(https?://[^\s]+)', html):
			print "................", i
			if i.startswith('https://stackoverflow.com/questions/'):
				print "############................", i
		return [url for url in re.findall(r'(https?://[^\s]+)', html) if url.startswith("https://stackoverflow.com/questions/")]

	def search(self, query):
		so_ids = []
		print 'Search Query: ', query
		for post_id in self.stackoverflow_questions(query):
			print 'Post_id: ', post_id

			so_id = post_id.split("/")[4]
			if so_id not in []:# ["299495", "41107", "151777", "160970", "240546", "320542", "304268", "333363", "26305", "14617"]:
				so_ids.append(so_id)
			else:
				print "Exclude", so_id

		print "SO_IDs: ", so_ids
		return so_ids

class GoogleAjaxSearch:
	def search(self, query):
		query = query.replace(" ", "+")
		url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s&rsz=large" % query
		print "Google Query: ", url 
		so_ids = []

		print "Before request"
		r = requests.get(url)
		print "Google JSON", r.json()
		results = r.json()["responseData"]["results"]
		for rank, res in enumerate(results[:5]):
			if res["url"].startswith("http://stackoverflow.com/questions/"):
				so_id = res["url"].split("/")[4]
				#so_ids.append({"id": so_id, "weight": len(results) - rank})


				if so_id not in []:# ["299495", "41107", "151777", "160970", "240546", "320542", "304268", "333363", "26305", "14618"]:
					so_ids.append(so_id)
				else:
					print "Excluded posts"

		print "After request"
				
		return so_ids


if __name__ == '__main__':
	from time import time
	t = time()

	q = "file encrypt"
	q += "stackoverflow java"
	google = GoogleSearcher()
	print(google.search(q))
	print(time()-t)

	t = time()
	ajax = GoogleAjaxSearch()
	print ajax.search(q)
	print(time()-t)



