from subprocess import call, Popen
from urllib2 import urlopen
import requests
from os import makedirs, walk, remove, listdir, stat, rename
from os.path import isdir, join, getmtime, abspath
from pymysql import connect

from time import strftime, gmtime



urls = [
	"https://github.com/spring-projects/spring-framework",
	"https://github.com/aporter/coursera-android",
	"https://github.com/jfeinstein10/SlidingMenu",
	"https://github.com/purplecabbage/phonegap-plugins",
	"https://github.com/libgdx/libgdx",
	"https://github.com/elastic/elasticsearch",
	"https://github.com/loopj/android-async-http",
	"https://github.com/netty/netty",
	"https://github.com/spring-projects/spring-boot",
	"https://github.com/facebook/facebook-android-sdk",
	"https://github.com/square/picasso",
	"https://github.com/rsirres/Sourcerer"
]

# Make sure you have git installed
# TODO: Determine number of files
# TODO: Determine number of LOC
# Create json file with METADATA: Crawling DateTime, URL, repository name, repository owner

def many(cur):
	while True:
		results = cur.fetchmany(10)
		if not results:
			break
		for result in results:
			yield result


import hashlib
def md5(s):	
	return hashlib.md5(s).hexdigest()

def read_file(path):
	with open(path, "r") as f:
		return f.read()

class GitCrawler:

	def __init__(self, home="/Users/Raphael/Downloads/GitArchive"):
		self.base = home
		self.home_path = "%s/%s" % (home, strftime('%d.%m.%Y'))
		
		self.conn = None

	def start(self):

		if not isdir(self.home_path):
			makedirs(self.home_path)

		self.conn = connect(host='localhost', port=3306, user='root', passwd='', db='Github')
		""" Retrieves Github API urls from MySQL Github Archive and check if repo has been forked at least once """
		sql = "SELECT url FROM Github.projects WHERE language = 'Java' AND forked_from IS NULL AND deleted = 0 LIMIT 10001,5000;"#5001,5000; 

		cur = self.conn.cursor()
		cur.execute(sql)

		for row in many(cur):
			url = row[0]
			
			self.clone_repo(url)
		


	def is_forked(self, url):
		try:
			res = requests.get(url, auth=('rsirres', '6e0dc35a466c646bda02865a3def298447a5827e'))
			data = res.text.encode("utf-8")

			num_forks = data.split('"forks":')[1].split(",")[0].strip()
			print num_forks != "0"

		except Exception as e:
			print "Repository is probably unavailable or you reached the limit of your GitHub requests"
			return False

		return num_forks != "0"

	#TODO: Add time and date of download
	def clone_repo(self, url):
		
		project_name = url.split("/")[-1]
		username = url.split("/")[-2]

		new_url = "https://github.com/%s/%s" % (username, project_name)
		project_dir = "%s/%s_%s" % (self.home_path, username, project_name)
		
		if not isdir(project_dir) and self.is_forked(url):
			print "Clone: %s" % url
			makedirs(project_dir)
			call(["git", "clone", new_url], cwd=project_dir)
			self.retain_java_files(project_dir)
		else:
			print "Project: %s already exists." % project_dir

	def retain_java_files(self, directory):
		from multiprocessing import Process
		def remove_non_java_files(directory):	

			non_java_files = (join(dirpath, f)
		    for dirpath, dirnames, files in walk(directory)
		    for f in files if not f.endswith('.java'))
			
			for non_java_file in non_java_files:
				remove(non_java_file)

		p = Process(target=remove_non_java_files, args=(directory,))
		p.start()

	def stats(self):
		files = (join(dirpath, f)
		    for dirpath, dirnames, files in walk(self.base)
		    for f in files)
		
		num_files = 0
		duplicates = 0
		loc = 0

		file_hash_set = set()
		for f in files:
			try:
				f_content = read_file(f)
				h = md5(f_content)

				if h in file_hash_set:
					duplicates += 1
				else:
					file_hash_set.add(h)

				loc += f_content.count('\n')


				num_files += 1
			except:
				pass
			


		print "Number of files: %s Duplicates: %s, LOC: %s" % (num_files, duplicates, loc)

	def test(self):
		import time
		dirs = listdir("%s/%s" % (self.base, "erh_mongo-irc"))[:10]
		for d in dirs:
			if not d.startswith("."):
				path = "%s/%s" % (self.base, d)
				if time.time() - getmtime(path) < 24 * 3600:
					print path 


	def creation_date(self, path):
		# path = "%s/%s" % ("/Users/Raphael/Downloads/GitArchive", "erh_mongo-irc")
		t = getmtime(path)
		return strftime("%d.%m.%Y", gmtime(t))

		
	
def iter_dirs():
	crawler = GitCrawler()
	# crawler.clone_repo("https://api.github.com/repos/schatten/schatten.github.com")
	#crawler.test()

	base = "/Users/Raphael/Downloads/GitArchive"
	dirs = listdir(base)
	for d in dirs:
		if not d.startswith(".") and not d.endswith(".2015"):
			source_path = "%s/%s" % (base, d)
			date_str = crawler.creation_date(source_path)

			target_path = "%s/%s/%s" % (base, date_str, d )
			#print source_path, target_path
			rename(source_path, target_path)

if __name__ == '__main__':

	crawler = GitCrawler()
	# crawler.clone_repo("https://api.github.com/repos/schatten/schatten.github.com")
	#crawler.test()
	crawler.stats()

			







	
	
	
