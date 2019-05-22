# Spiderforce
Given a [list of] domain[s], spiderforce parses all text to create a wordlist (optionally filtered by a given regex), and optionally spiders (in scope) links to a given depth (or until a keyboard interrupt is given). The resulting wordlist can be used to brute force passwords, subdomains, subdirectories, etc.

---

Installation (requires python3.7+):

```
git clone https://github.com/daniellohrey/spiderforce.git
[sudo] pip install -r requirements.txt
```

---

Basic usage:
* Scrape a single webpage and print wordlist to stdout:

   `spiderforce.py -d domain.com`

* Scrape a list of domains from a file and print to stdout:

   `spiderforce.py -D domainlist.txt`

* Spider all links on a single domain (until pages are exhausted or a KeyboardInterrupt is received)

   `spiderforce.py -d domain.com -m 0`

* Print results to a file instead of stdout

   `spiderforce.py -d domain.com -w passwordlist.txt`

---

All options:
```
spiderforce.py [-h] (-d DOMAIN | -D DOMAINS) [-s SCOPE] [-o OUTSCOPE] [-n] 
		[-w WRITE] [-m MAX_DEPTH][-t THREADS] [-r REGEX] [-v]
```

Arguments:

  -h, --help
 * Show this help message and exit

  -d DOMAIN, --domain DOMAIN
 * Single domain to use

  -D DOMAINS, --domains DOMAINS
  * File with list of domains to use

  -s SCOPE, --scope SCOPE
  * File containing in-scope strings, defaults to [list of] domain[s] if not specified
  
  -o OUTSCOPE, --outscope OUTSCOPE
  * File containing out of scope strings

  -n, --noscope         
  * Flag to set all urls to be in-scope

  -w WRITE, --write WRITE
  * Write wordlist to file instead of stdout

  -m MAX_DEPTH, --max_depth MAX_DEPTH
  * Maximum depth of links to spider (defaults to 1 (no spidering), 0 for infinite spidering)

  -t THREADS, --threads THREADS
  * Number of worker threads to use, defaults to 8

  -r REGEX, --regex REGEX
  * Regex used to filter words added to wordlist

  -v, --verbose
  * Print domains as they are parsed
  
A url is defined to be in scope if it contains at least one in-scope string, and no out of scope strings. Use the -n option to make all urls in scope. (Default scope is list of domains, if not specified.)

---

Classes:

* scope.py

   Defines a scope object, which takes a list of in-scope strings, and optionally a list of outscope strings, and exposes a method to test whether a string falls in or out of scope. Also contains a dummy No-scope class which always returns true when testing scope.

* spider.py

   Defines a spider class which requires, any number of domains, a scope object, a wordlist object, an optional number of worker threads to use (defaults to 8), an optional maximum depth of links to spider (defaults to 1, ie just the given domains) and options for verbosity and run on creation, and exposes a run method which runs the spidering until the queue is exhausted (or an interrupt is triggered) and fills the wordlist with data.

* wordlist.py

   Defines a wordlist, implemented as a set, which exposes a method to add items to the wordlist, filtered by a given regex (if specified).
	
* spiderforce.py

   Wrapper with command line argument parsing.
   
---
   
I feel things are in a good, working state and the original design goals have been statisfied so further updates will be sporatic at best. That said, if you have any ideas for features, or encounter any issues, please reach out and I'll see what I can do.
