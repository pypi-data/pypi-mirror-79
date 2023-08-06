# Generate a pseudo diceware password
# DO NOT USE IT FOR STRONG CRYPTOGRAPHIC PURPOSE!

from random import choice
import sys
import os

# set the wordlist path
wordlist = "objects/wordlist.txt"

parent_dir = os.path.abspath(os.path.dirname(__file__))
wordlist_path = os.path.join(parent_dir, wordlist)

def diceware(N, wordlist=wordlist_path, separator="", camelcase=True):
	with open(wordlist, "r") as f:
		words = f.read().split('\n')
		out = []
		for i in range(N):
			word = choice(words)
			if camelcase:
				word = word.capitalize()
			out.append(word)
		return separator.join(out)
