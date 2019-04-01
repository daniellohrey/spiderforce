#class definition for spider

from queue import Queue
from queue.error import Empty
from threading import Thread, Event
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import scope

class Spider():
	#takes any number of initial urls and a scope object (from scope.py)
	#optionally can speficify how many threads to use and when to stop queueing links after going so deep
	def __init__(self, *urls, scope, max_depth = -1, threads = 4):
		self._scope = scope
		self._queue = SimpleQueue()
		self._max_depth = max_depth
		self._threads = threads
		self._done = []
		self._words = []
		for url in urls:
			ut = (url, 0)
			self._queue.put(url)
			self._done.append(url)

	#worker thread function
	#takes urls from the queue, parses and adds links to queue, records urls and scrapes text
	def worker(self, event):
		while event.is_set():
			try:
				url, depth = self._queue.get(timeout = 3)
			except Empty:
				continue #try again if we didnt get anything, queue may be empty, in which case well exit soon
			if self._max_depth > 0 and depth > self._max_depth:
				continue #weve gone far enough, son
			try:
				resp =  urlopen(url)
				html = resp.read()
			except HTTPError as e:
				continue #catch 404s etc.
			except URLError as e:
				#you done messed up
				continue
			#everything is fine so far
			if url not in self._done:
				self._done.append(url)
			else:
				continue #weve already done this one
			q_links(html)
			g_words(html)

	#creates and runs threads
	def run(self):
		threads = []
		event = Event()
		event.set() #event to signal threads to exit
		for i in range(self._threads):
			t = Thread(target = worker, args = (event,))
			t.start()
			threads.append(t)
		try:
			while True:
				if self._queue.empty():
					sleep(2) #if queue is empty wait a second and check again, if its still empty were probably done
					if self._queue.empty():
						break
				else:
					sleep(5)
		except KeyboardInterrupt:
			pass #get out of loop and signal exit on keyboard interrupt
		event.clear()
		for t in threads:
			t.join() #wait for threads to exit
