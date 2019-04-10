#Spiders a [list of] domain[s] and generates a wordlist based on all text found

import argparse
import spider
import scope
import sys

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
parser.add_argument("-w", "--write", help = "File to write wordlist out to instead of stdout")
parser.add_argument("-m", "--max_depth", type = int, help = "Maximum depth of links to spider")
parser.add_argument("-t", "--threads", type = int, help = "Number of worker threads to use, defaults to 4")
args = parser.parse_args()

if args.domain:
	urls = [fix_domain(args.domain)]
	if not args.scope:
		#if theres no scope just use the domain name with no path
		args.scope = urls[0].split("://")[1].split("/")[0]
elif args.domains:
	if not args.scope:
		#if we dont have a scope then just use the list of domains
		args.scope = args.domains
	with open(args.domains, "r") as f:
		urls = []
		for line in f.readlines():
			urls.append(fix_domain(line))

if args.outscope:
	sc = scope.Scope(args.scope, args.outscope)
else:
	sc = scope.Scope(args.scope)

if args.max_depth and args.threads:
	sp = spider.Spider(*urls, scope = sc, max_depth = args.max_depth, threads = args.threads)
elif args.max_depth:
	sp = spider.Spider(*urls, scope = sc, max_depth = args.max_depth)
elif args.threads:
	sp = spider.Spider(*urls, scope = sc, threads = args.threads)
else:
	sp = spider.Spider(*urls, scope = sc)

sp.run()

if args.write:
	with open(args.write, "w") as f:
		for word in sp.wordlist:
			f.write(word)
else:
	for word in sp.wordlist:
		print(word)
