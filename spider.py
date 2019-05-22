#class definition for spider

from queue import SimpleQueue, Empty
from threading import Thread, Event
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from time import sleep
from scope import Scope, NoScope
from wordlist import Wordlist

class Spider():
	#takes any number of initial urls and an optional scope object
	#optionally can speficify how many threads to use, when to stop queueing links and regex to use to filter wordlist
	def __init__(self, *urls, scope = None, max_depth = 1, threads = 8, run = False, verbose = False, wordlist = None):
		self._scope = scope
		self._queue = SimpleQueue()
		self._max_depth = max_depth
		self._threads = threads
		self._done = set()
		self._words = wordlist
		for url in urls:
			u_d = (url, 1)
			self._queue.put(u_d)
		if run:
			self.run()

	@property
	def urllist(self):
		return self._done

	@property
	def urls(self):
		for url in self._done:
			yield url

	@property
	def wordlist(self):
		return self._words.wordlist

	@property
	def words(self):
		for word in self._words.next:
			yield word

	#worker thread function
	#takes urls from the queue, parses and adds links to queue, records urls and scrapes text
	def worker(self, event):
		while event.is_set():
			try:
				url, depth = self._queue.get(timeout = 1)
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
				continue #mistake in url, skip
			if url not in self._done:
				self._done.add(url)
			else:
				continue #weve already done this one
			if self._verbose:
				print("Parsing " + url)
			#improve post spidering with post requests, etc.
			self.q_links(html, url, depth)
			self.g_words(html)

	#creates and runs threads
	def run(self):
		print("starting threads...")
		threads = []
		event = Event()
		event.set() #event to signal threads to exit
		for i in range(self._threads):
			t = Thread(target = self.worker, args = (event, ))
			t.start()
			threads.append(t)
		try:
			print("running... (ctrl-c to quit)")
			sleep(2) #dont accidently quit initially
			while True:
				if self._queue.empty():
					sleep(1) #double check queue is empty
					if self._queue.empty():
						break
				else:
					sleep(2)
		except KeyboardInterrupt:
			pass #signal exit on keyboard interrupt
		event.clear()
		print("Waiting for threads to exit... (ctrl-c to force quit)")
		for t in threads:
			t.join() #wait for threads to exit

	#searches html for links and adds them to the queue if they are in scope (unless they exceed the maximum depth)
	def q_links(self, html, url, depth):
		if self._max_depth > 0 and depth >= self._max_depth:
			return #dont want to add links that are too deep
		depth += 1
		#add support for other parsers
		soup = BeautifulSoup(html, features = "html.parser")
		links = soup.find_all('a')
		for link in links:
			try:
				if "?" in link:
					link["href"] = link["href"].split("?")[0]
				if "#" in link:
					link["href"] = link["href"].split("#")[0]
				link = urljoin(url, link["href"])
				if self._scope.in_scope(link):
					u_d = (link, depth)
					self._queue.put(u_d)
			except Exception as e:
				pass
			
	#gets all text from html and adds words to wordlist
	def g_words(self, html):
		wl = set()
		#add support for other parsers
		soup = BeautifulSoup(html, features = "html.parser")
		for string in soup.stripped_strings:
			words = string.split()
			wl.update(words)
		self._words.add(wl)

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
