#class to hold a list of unique strings, matching a regex, implemented as a set
import re

class WordList():
	def __init__(self, regex):
		if regex:
			self._pat = re.compile(regex)
		else:
			self._pat = None
		self._wl = set()

	@property
	def wordlist(self):
		return self._wl

	@property
	def next(self):
		for word in self._wl:
			yield word

	def add(self, new):
		if self._pat == None:
			self._wl.update(new)
		else:
			for item in new:
				match = self._pat.search(item)
				if match:
					self._wl.add(match[0])
