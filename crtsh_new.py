#!/usr/bin/env python3


import requests, json
import sys 
import argparse

#-----functions-----
def Remove(duplicate):
	cleared_list = []
	for num in duplicate:
		if num in duplicate:
			cleared_list.append(num)
	return cleared_list

def str2bool(v):
	if isinstance(v, bool):
		return v
	if v.lower() in ('yes', 'true', 't', 'y', '1'):
		return True
	elif v.lower() in ('no','false','f','n', '0'):
		return False
	else:
		raise argparse.ArgumentTypeError('Boolean value expected.')

def niceout(givenlist, domain, outbool):
	extractedsubdomains = []
	output = []
	# at first extract only subdomains from json response
	for i in givenlist:
		extractedsubdomains.append(i['name_value'])
	#sort and delete duplicates
	extractedsubdomains.sort()
	for x in extractedsubdomains:
		if x not in output:
			output.append(x)
	#print on screen
	for elem in output:
		print(elem)
	if outbool is True:
		filename = str(domain.split('.', 1)[0]) + '.txt'
		print("Domains saved to " + filename)
		filed = open(filename, 'w')
		for elem in output:
			filed.write(elem + '\n')
		filed.close


def verboseout(domain): #prints the whole json to cli
	print(json.dumps(certshAPI().search(domain), indent=2))
	 

#-----classes-----
class certshAPI(object):
	def search(self, domain, wildcard=True):
		base_url = "https://crt.sh/?q={}&output=json"
		if wildcard:
			domain= "%25.{}".format(domain)
		url = base_url.format(domain)
		print(url)
		ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
		req = requests.get(url, headers={'User-Agent': ua})

		if req.ok:
			try:
				content = req.content.decode('utf-8')
				data = json.loads("{}".format(content.replace('}{', '},{')))
				return data
			except Exception as err:
				print("Error getting informations")
		return None


#----- The Main Thing -----
parser = argparse.ArgumentParser(description='This script queries crt.sh for a given domain and parses the output.')
parser.add_argument('-domain', type=str, required=True, help='Enter a value for target domain.')
parser.add_argument('--verbose', action='store_true', help='Verbose output, that means the complete json-response from crt.sh.')
parser.add_argument('--out', type=str2bool, help='Writes output in file for later use.')
args = parser.parse_args()

if  args.verbose == True:
	verboseout(args.domain)
else:
	data = certshAPI().search(args.domain)
	niceout(data, args.domain, args.out)

	
