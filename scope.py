#implements scope class with exposes in_scope() which takes a string and returns True if it is a substring of at least one in scope item and matches no out of scope items, false otherwise (case insensitive)
#takes string or file for in scope, and optionally string or file for out scope

import os
import sys

class Scope:
	def __init__(self, inscope, *args):
		self._inscope = []
		self._outscope = []
		if os.path.isfile(inscope):
			with open(inscope, "r") as f:
				for line in f.readlines():
					line = line.strip()
					self._inscope.append(line.lower())
		else:
			self._inscope.append(inscope.lower())
		if len(args) == 1:
			if os.path.isfile(args[0]):
				with open(args[0], "r") as f:
					for line in f.readlines():
						line = line.strip()
						self._outscope.append(line.lower())
			else:
				self._outscope.append(args[0].lower())
		elif len(args) > 1:
			raise Exception("Too many arguments to Scope()")

	def _incheck(self, string):
		for item in self._inscope:
			if item in string:
				return True
		return False

	def _outcheck(self, string):
		if len(self._outscope) == 0:
			return True
		for item in self._outscope:
			if item in string:
				return False
		return True

	def in_scope(self, string):
		string = string.lower()
		if self._incheck(string) and self._outcheck(string):
			return True
		return False

if __name__ == "__main__":
	if len(sys.argv) == 3:
		scope = Scope(sys.argv[1])
		_tests = sys.argv[2]
	elif len(sys.argv) == 4:
		scope = Scope(sys.argv[1], sys.argv[2])
		_tests = sys.argv[3]
	else:
		print("Test the scope module - in scope items have at least one inscope string as a substring and no outscope strings a substring (case insensitive)")
		print("Usage: python scope.py inscope [outscope] tests")
		print("inscope - string or file to include in scope")
		print("outscope - string or file to exclude from scope (optional)")
		print("tests - string or file of test strings to check scope of")
	tests = []
	if os.path.isfile(_tests):
		with open(_tests, "r") as f:
			for line in f.readlines():
				line = line.strip()
				tests.append(line)
	else:
		tests.append(_tests)
	for test in tests:
		if scope.in_scope(test):
			result = "in scope"
		else:
			result = "out of scope"
		print(f"{test} - {result}")
