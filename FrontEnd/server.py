#!/usr/bin/env jython
#-*- coding: utf-8 -*-
from flask import Flask, Markup, render_template, send_from_directory, request
from highlight import highlight_files
from GitSearchItem import GitSearchItem
from GitSearchResult import GitSearchResult
from GitSearchFile import highlight_file
# import sys
# sys.setrecursionlimit(800000)

from collections import namedtuple
from GitSearcher import StackoverflowSearcher, GitHubSearcher, GoogleStackoverflowSearcher

from utils import read_file

import traceback

# TODO: Query Index
# TODO: Ranking
# open files and highlight
# TODO: Return results back to user

INDEX_BASE_PATH = "/home/ubuntu/Desktop/CoCaBu/GitSearch/Indices/" #"/Users/Raphael/Downloads/"

app = Flask(__name__, static_folder='static')
def to_q(path):
	from urllib import quote_plus
	return quote_plus(path)

app.jinja_env.globals.update(to_q=to_q)

@app.route("/")
def index(name=None):
	
	query = request.args.get('q')
	evaluation = request.args.get("evaluation")

	try:

		if query:

			if evaluation:
				github_items = query_index2(query)
			else:
				github_items = query_index(query)
			git_search_result = GitSearchResult(github_items)
			for i in git_search_result.items:
				print "****************************", i.so_item.title			
			return render_template("search.html", name=query, git_search_result=git_search_result)
	except:
		print(traceback.format_exc())

	return render_template("index.html", name=name)


@app.route('/source')
def show_source():
	
	file_path = request.args.get('q')

	if file_path:
		html = highlight_file(file_path)
		return render_template("file.html", file_path=file_path, source = html)



@app.route('/<path:file_path>')
def static_proxy(file_path):

	# send_static_file will guess the correct MIME type
	return send_from_directory(app.static_folder, file_path)

def render_code_results(query):
	github_items = query_index(query)

	
	git_search_items = [ GitSearchItem(github_item) for github_item in github_items ]
	

	return git_search_items



def query_index(query):
	""" Returns a set of file paths relevant to given query """
	
	print "Stackoverflow Index"
	from time import time
	t = time()
	google = GoogleStackoverflowSearcher("%sstackoverflow_Co" % (INDEX_BASE_PATH)) #
	so_items = google.search(query, 5)
	print "stack items: ", so_items
	print "Google Request Time: %s" % (time()-t)
	t = time()

	github = GitHubSearcher("%sgithub" % (INDEX_BASE_PATH), query)
	github_items = github.more_like_this2(so_items)	

	#print "github_items", github_items

	print "GitSearch Request Time: %s" % (time()-t)

	return github_items

def query_index2(query):
	""" Returns a set of file paths relevant to given query """

	print "Evaluation Index"
	from time import time
	t = time()
	google = GoogleStackoverflowSearcher("%sevaluation201306" % (INDEX_BASE_PATH)) #
	so_items = google.search(query, 10)
	print "Google Request Time: %s" % (time()-t)
	t = time()

	github = GitHubSearcher("%sgithub" % (INDEX_BASE_PATH), query)
	github_items = github.more_like_this(so_items)	

	print "GitSearch Request Time: %s" % (time()-t)

	return github_items



if __name__ == "__main__":
	while True:
		try:
			app.run(host="0.0.0.0", port=4568)
		except Exception as e:
			print e

