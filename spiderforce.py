#Spiders a [list of] domain[s] and generates a wordlist based on all text found

import argparse
import spider
import scope
import sys

#prepends http:// if not present
def fix_domain(url):
	if "://" not in url:
		return "http://" + url
	return url

parser = argparse.ArgumentParser(description = "Spider a [list of] domain[s] and generate a wordlist based on all text found")
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument("-d", "--domain", help = "Domain to spider")
group.add_argument("-D", "--domains", help = "File with list of domains to spider")
parser.add_argument("-s", "--scope", help = "File containing in scope strings defaults to [list of] domain[s] if not specified")
parser.add_argument("-o", "--outscope", help = "File containing out of scope strings")
parser.add_argument("-n", "--noscope", action = "store_true", help = "Flag to set all strings to be in scope")
parser.add_argument("-w", "--write", help = "File to write wordlist out to instead of stdout")
parser.add_argument("-m", "--max_depth", type = int, default = -1, help = "Maximum depth of links to spider")
parser.add_argument("-t", "--threads", type = int, default = 8, help = "Number of worker threads to use, defaults to 8")
parser.add_argument("-r", "--regex", help = "regex used to filter additions to wordlist")
parser.add_argument("-v", "--verbose", action = "store_true", help = "Print domains as they are parsed")
args = parser.parse_args()

#urls is list of domains to spider
if args.domain:
	urls = [fix_domain(args.domain)]
elif args.domains:
	with open(args.domains, "r") as f:
		urls = []
		for line in f.readlines():
			urls.append(fix_domain(line))
else:
	print("No domains to spider")
	sys.exit()

#sc is scope
if args.noscope:
	sc = None
else:
	#i_sc is inscope
	if args.scope is not None:
		i_sc = args.scope #takes filename or list
	else:
		#if theres no in scope just use the list of domain names
		i_sc = []
		for url in urls:
			#split off http[s]:// and anything after a /
			i_sc.append(url.split("://")[1].split("/")[0])
	if args.outscope is not None:
		sc = scope.Scope(i_sc, args.outscope)
	else:
		sc = scope.Scope(i_sc)

sp = spider.Spider(*urls, scope = sc, max_depth = args.max_depth, threads = args.threads, regex = args.regex, verbose = args.verbose)
sp.run()

if args.write:
	with open(args.write, "w") as f:
		print("writing to file...")
		for word in sp.next:
			f.write(word + "\n")
else:
	for word in sp.next:
		print(word)
