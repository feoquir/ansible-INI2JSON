#!/usr/bin/env python
#
#	A quick file converter example which takes a file from
#	the argument and runs it through the ini2json actual
#	translator
#

import re, argparse, sys
from helper.ini2json import *

def main():
	try:
		ini_file = open("{}".format(sys.argv[1]),"r")
	except:
		print("Please call the script with a file")
		exit()
	print(ini2json(ini_file.read()))

if __name__ == '__main__':
	main()



