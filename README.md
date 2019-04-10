# spiderforce
Spiders a domain and scrapes pages to build a wordlist.

Runs until all inscope links have been exhausated up until the maximum depth (if specified), or until a keyboard interrupt is triggered.
A url is in scope if at least one inscope string is a substring and no outscope string is a substring.

usage: spiderforce.py [-h] (-d DOMAIN | -D DOMAINS) [-s SCOPE] [-o OUTSCOPE]
                      [-w WRITE] [-m MAX_DEPTH] [-t THREADS]

Spider a [list of] domain[s] and generate a wordlist based on all text found

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to spider
  -D DOMAINS, --domains DOMAINS
                        File with list of domains to spider
  -s SCOPE, --scope SCOPE
                        File containing in scope strings, defaults to [list of]
                        domain[s] if not specified
  -o OUTSCOPE, --outscope OUTSCOPE
                        File containing out of scope strings
  -w WRITE, --write WRITE
                        File to write wordlist out to instead of stdout
  -m MAX_DEPTH, --max_depth MAX_DEPTH
                        Maximum depth of links to spider
  -t THREADS, --threads THREADS
                        Number of worker threads to use, defaults to 4

Classes:
	scope.py - defines a scope object, which takes a list of inscope strings, and optionally a list of outscope strings, and exposes a method to test whether a string falls in or out of scope.
	spider.py - defines a spider class, which any amount of domains, a scope (defaults to everything being in scope), an optional number of worker threads to use (default 4) and an optional maximum depth of links to spider, and exposes a run method which runs the spidering until the queue is exhausted (or an interrupt is triggered) and fills the wordlist with data.

spiderforce.py is a wrapper for the spider class with command line argument parsing.
