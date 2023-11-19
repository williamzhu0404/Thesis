# Import the beautifulsoup
# and request libraries of python.

from pathlib import Path


import re

import numpy as np
import pandas as pd

import requests
import bs4

# Make two strings with default google search URL
# 'https://google.com/search?q=' and
# our customized search keyword.
# Concatenate them


def google(txt):
	print(txt)
	url = 'https://google.com/search?q=' + txt
	request_result=requests.get( url )
	soup = bs4.BeautifulSoup(request_result.text,
						"html.parser")
	heading_object=soup.find_all( 'h3' )
	for info in heading_object:
		print(info.getText())
		print("------")



PAUSE_SIGNAL = 9


def pause(pd_series, ind, file_name):
	pd_series[ind] = 8
	print(ind, pd_series[ind])
	pd_series.to_pickle(file_name)
	exit()


leg_name_master = pd.read_pickle("name_match.pkl")


file = Path("flag.pkl")
if file.exists():
	print("file found")
	investigate = pd.read_pickle("flag.pkl")
else:
	investigate = pd.Series(9, index=leg_name_master.index)



party_quit = "{} 退黨"
party_admit = "{} 入黨"
party_start = "{} 創黨"

search_txts_format = [party_quit, party_admit, party_start]

print(investigate)


for i, name in enumerate( leg_name_master.name):	
	print(i, investigate[i])
	if investigate[i] > 7:
		keep_searching = True
		print(i, name)
		print(name)
		print("Google search begins")
		for search in search_txts_format:
			if keep_searching:
				txt = search.format(name)
				google(txt)
				flag = input("Does the Google search result needs further investigation? [y/n/p]")
				if flag.lower() == 'n':
					keep_searching = False
					suspect = input("Has the legislator been disloyal to the party?[y/n/p]")
					if suspect.lower() == 'y':
						investigate[i] = 2	
						print("This legislator's party record is sus.")
					if suspect.lower() == 'n':
						investigate[i] = 1	
						print("This legislator's party record is legit.")
					elif suspect.lower() == 'p':
						pause(investigate, i, "flag.pkl")
				elif flag.lower() == 'p':
					pause(investigate, i, "flag.pkl")


investigate.to_pickle("flag.pkl")


