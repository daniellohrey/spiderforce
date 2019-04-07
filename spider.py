#class definition for spider

from queue import SimpleQueue
from queue import Empty
from threading import Thread, Event
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup
from time import sleep
#from error import LinkError #dont need anymore
from scope import Scope, NoScope
from re import search

class Spider():
	#takes any number of initial urls and an optional scope object
	#optionally can speficify how many threads to use and when to stop queueing links
	def __init__(self, *urls, scope = None, max_depth = -1, threads = 4):
		if scope is not None:
			self._scope = scope
		else:
			self._scope = NoScope()
		self._queue = SimpleQueue()
		self._max_depth = max_depth
		self._threads = threads
		self._done = []
		self._words = [] #update to use wordlist class
		for url in urls:
			u_d = (url, 1) #possibly need to start at 1
			self._queue.put(u_d)

	@property
	def urls(self):
		return self._done

	@property
	def wordlist(self):
		return self._words

	#worker thread function
	#takes urls from the queue, parses and adds links to queue, records urls and scrapes text
	def worker(self, event):
		while event.is_set():
			try:
				url, depth = self._queue.get(timeout = 3)
			except Empty:
				continue #try again if we didnt get anything, queue may be empty, in which case well exit soon
			try:
				#may need to add support for https
				req = Request(url)
				resp = urlopen(req)
				html = resp.read()
			except HTTPError as e:
				continue #catch 404s etc.
			except URLError as e:
				continue #you done messed up
			if url not in self._done:
				self._done.append(url)
			else:
				continue #weve already done this one
			self.q_links(html, url, depth)
			self.g_words(html)

	#creates and runs threads
	def run(self):
		threads = []
		event = Event()
		event.set() #event to signal threads to exit
		for i in range(self._threads):
			t = Thread(target = self.worker, args = (event, ))
			t.start()
			threads.append(t)
		try:
			sleep(3) #hacky sleep so we dont accidently quit initially
			while True:
				if self._queue.empty():
					sleep(2) #if queue is empty wait and check again, if its still empty were probably done
					if self._queue.empty():
						break
				else:
					sleep(5)
		except KeyboardInterrupt:
			pass #get out of loop and signal exit on keyboard interrupt
		event.clear()
		for t in threads:
			t.join() #wait for threads to exit

	#searches html for links and adds them to the queue if they are in scope (unless the exceed the maximum depth)
	def q_links(self, html, url, depth):
		if self._max_depth > 0 and depth >= self._max_depth:
			return #dont want to add links that are too deep
		depth += 1 #we have to go deeper *stares intently*
		soup = BeautifulSoup(html, features = "html.parser")
		links = soup.find_all('a')
		for link in links:
			try:
				#may need some preprocessing
				link = urljoin(url, link["href"])
				u_d = (link, depth)
				if self._scope.in_scope(link):
					self._queue.put(u_d)
			except Exception as e:
				pass
			
	#gets all text from html and adds words to wordlist
	def g_words(self, html):
		soup = BeautifulSoup(html, features = "html.parser")
		for string in soup.stripped_strings: #alt soup.get_text(strip=True)
			words = string.split()
			for word in words:
				#wordlist processing, move out of here
				m = search("[-.a-zA-Z0-9]+", word)
				if m:
					word = m[0]
				else:
					continue
				if word not in self._words:
					self._words.append(word)

if __name__ == "__main__":
	import sys
	if len(sys.argv) == 3:
		spider = Spider(sys.argv[1], max_depth = int(sys.argv[2]))
	elif len(sys.argv) == 2:
		spider = Spider(sys.argv[1])
	else:
		print("spider.py domain [depth]")
		sys.exit()

	spider.run()
	for url in spider.urls:
		print(url)
	for word in spider.wordlist:
		print(word)
