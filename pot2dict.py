# coding=utf8

# TODO - automatic hash recognizing.

import re
import argparse
import os
import sys

def epilogue():
	return """ 

#		| Hash-type	| Example                            
=================================
0		| MD5		| 24a5478cc7c75376e36b3a7a45ae13b2:vodka
100		| SHA1		| c99eb3910ba3d7b681ea3e6040ad649da5e6f4a7:vodka
99998	| Email		| ema+il@google.com:vodka
"""

def exitProgram(errorCode):
	print errorCode
	sys.exit()

def checkExistFile(fileName):
	return os.path.exists(fileName)

def getArgs():
	parser = argparse.ArgumentParser(description='Parse Hascat potfile output to create a dictionary.', epilog=epilogue(), formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-p', '--potfile-path', type=str, help='Specific path to potfile', required=True)
	parser.add_argument('-o', '--outfile', type=str, help='Define outfile for dictionary', required=True)
	parser.add_argument('-m', '--hash-type', type=str, help='Hash-type, see references below', required=True)
	return parser.parse_args()	

def copyToMemory(fileName, hashType):
	if checkExistFile(fileName):
		cacheBlob = 1024*1024
		blob = open(fileName, 'rb')
		lines = blob.read(cacheBlob)
		while lines:
			result = findMatch(lines, hashType)
			yield result
			lines = blob.read(cacheBlob)
	else:
		exitProgram("File name correct? See help for more information")

def findMatch(blob, mode):	

	if hashType(mode):
		return re.findall(hashType(mode), blob, re.MULTILINE)
	else:
		exitProgram("Hash-type not found. See help for more information")

def writeToFile(outFile, results):
	for _ in xrange(len(results)):
		open(outFile, "a").write("\n".join(results[_]))
	exitProgram("Done")

def hashType(mode):
	option = {
		"0": "^[a-fA-F\d]{32}:(.*)",
		"100": "^[a-fA-F\d]{40}:(.*)",
		"99998": "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*:(.*)",
	}

	return option.get(mode, False)

if __name__ == "__main__":

	args = getArgs()
	results = list(copyToMemory(args.potfile_path, args.hash_type))
 	writeToFile(args.outfile, results)
