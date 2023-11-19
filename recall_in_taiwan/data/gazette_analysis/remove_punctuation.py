from pathlib import Path

import fileinput





folder = "/Users/williamzhu/Thesis/recall_in_taiwan/data/electoral_data/votedata/voteData/20120114-總統及立委_1"


text_to_search = "'"
replacement_text = ''


p = Path(folder)
for filename in p.glob('**/*.csv'):
	with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
		for line in file:
			print(line.replace(text_to_search, replacement_text), end='')

