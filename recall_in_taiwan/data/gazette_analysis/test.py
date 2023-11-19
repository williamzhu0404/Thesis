import pdfplumber

import re

import numpy as np
import pandas as pd

def read_gazette(txt):
	ind1 = txt.find('\n')
	ind2 = txt.rfind('\n')
	return txt[ind1+1:ind2+1]




def name_interpret(line):
	names = line.split(" ")
	# Exceptions to handle: two-character names, Han name with indigenous name
	pass


 
pdf_1 = pdfplumber.open("LCIDC01_1060401.pdf")

pdf =  pdfplumber.open("LCIDC01_1122005.pdf") 

txts_1 = [read_gazette( pdf_1.pages[i].extract_text() ) for i in range(4, 31)]


sample_txts = "".join(txts_1)


sample = txts_1[0] + txts_1[1]

chn_char = "[\u4E00-\u9FFF]"
chn_char_1 = "[一-鿆]"
eng_lower = "[a-z]"
eng = "[a-zA-Z]"

name_match   = "{}+".format(chn_char)
name_match_1 = "{0}+.*?{1}".format(chn_char, eng_lower)

chn_name = "[一-鿆].+?(?= |\n)"

chn_name_ind_ext_template = "({0}.+?(?= {0}|\n|$| [A-Z][a-z]* [A-Z][a-z]*)|[A-Z][a-z]* [A-Z][a-z]*)"

leg_name = chn_name_ind_ext_template.format(chn_char_1)


motion_pattern = ""

rcv_begin = "表決結果名單："

rcv_end = "主席"

rcv_pattern = "{0}.*?{1}".format(rcv_begin, rcv_end)

rcv_begin_1 = "現在進行表決"
rcv_end_1   = "[政|本]院"


rcv_begin_2 = "現在進行表決"
rcv_end_2   = "(主席|[政|本]院)"


rcv_begin_3 = "現在進行(重付)*?表決"
rcv_end_3   = "(主席|[政|本]院)"

rcv_pattern_1 = "{0}.*?{1}".format(rcv_begin_1, rcv_end_1)

rcv_pattern_2 = "{0}.*?{1}".format(rcv_begin_2, rcv_end_2)

rcv_pattern_3 = "{0}.*?{1}".format(rcv_begin_3, rcv_end_3)

rcv_pattern_4 = "{0}.*?(?={1})".format(rcv_begin_3, rcv_end_3)


indigenous_name_pattern = ""


match = re.search(rcv_pattern, sample , re.DOTALL)

narrow_match = re.findall(rcv_pattern, sample_txts, re.DOTALL)


broad_match = re.findall(rcv_pattern_1, sample_txts, re.DOTALL)
adjusted_match = re.findall(rcv_pattern_3, sample_txts, re.DOTALL)



first, last = 55, 63

txts = [ read_gazette( pdf.pages[i].extract_text()     ) for i in range(first - 1, last +1) ]





