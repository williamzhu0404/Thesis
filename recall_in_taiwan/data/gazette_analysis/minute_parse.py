import pdfplumber

import re

import numpy as np
import pandas as pd

import dateparser
from datetime import datetime

from pathlib import Path


from plyer import notification





# Regex pattern variables and match functions

RCV_BEGIN = "本次會議各項記名表決結果名單："


CHN_CHAR = "[\u4E00-\u9FFF]"
CHN_CHAR_1 = "[一-鿆]"
ENG_LOWER = "[a-z]"
ENG = "[a-zA-Z]"


ROC_YEAR_ZERO = 1911



name_match   = "{}+".format(CHN_CHAR_1)
name_match_1 = "{0}+.*?{1}".format(CHN_CHAR_1, ENG_LOWER)

chn_name = "{0}.+?(?= |\n)".format(CHN_CHAR_1)


##   ---***--- beware the ugly fullwidth forms of punctuations and characters

#chn_name_ind_ext_template_1 = "({1}{0}.+?(?= {0}|\n|$| [A-Z][a-z]* [A-Z][a-z]*)|[A-Z][a-z]* [A-Z][a-z]*)"
chn_name_ind_ext_template_2 = "({1}{0}.+?(?= {0}|\n|$| [A-Z][a-z]* ?[A-Z][a-z]*)|[A-Z][a-z]* ?[A-Z][a-z]*)"
chn_name_ind_ext_template = "({1}{0}.+?(?= {0}|\n|$| [A-Z][a-z]* ?[A-Z][a-z]*)|[A-Z][a-z]* ?[A-Z]?[a-z]*)"
leg_name = chn_name_ind_ext_template.format(CHN_CHAR_1, "")
title = "[\(（][0-9]+[\)）].+?(?=贊)"




title_ind = "\([0-9]+\)"
title_num = "(?<=[（\(])\d+(?=[）\)])" 


#REC_DELIMITERS_1 = "[\(（]\d+[\)）]「.+?(?=[\(（]|$)"
REC_DELIMITERS = "[\\(（]\d+[\\)）]「.+?(?=[\\(（]\d+[\\)）]|$)"


camp = "[贊反棄].者：[0-9]+"
camp_strength = "(?<=[贊反棄].者：)[0-9]+"





#combined = "{0}|{1}|".format(title, camp)
#combined_1 = "{0}|{1}|".format(title_1, camp)
combined_2 = "{}|".format(camp)

ext_search = chn_name_ind_ext_template.format(CHN_CHAR_1, combined_2)


TIME_MARK = "時 *間"
LOC_MARK = "地 *點"
ROC_TIME_LOC = "國.*?(?=\n[地出])"


ROC_YEAR = "民?國?\d{1,3}年"
#ROC_YEAR_NUM_1 = "(?<=國)\d{,4}(?=年)"
ROC_YEAR_NUM = "\d{,3}(?=年)"
ROC_DATE_FORMAT = "民?國?\d{,3}年?\d{1,2}月\d{1,2}[日號]"
CHN_MMDD_FORMAT = "\d{1,2}月\d{1,2}[日號]"


LEG_PRESENT_START = "出席委員 "
LEG_PRESENT_END = "\n委員出席 \d{1,3}人"
LEG_PRESENT_COUNT = "(?<=\n委員出席 )\d{1,3}(?=人)"

TERM_NUM = "(?<=立法院第)\d{1,3}(?=屆)"













legislator_infos = pd.read_csv("16_CSV_16_CSV.csv", parse_dates=[8, 13])


leg_9 = legislator_infos[legislator_infos.term == 9]["name"].drop_duplicates().sort_values()

leg_name_master = pd.read_pickle("name_match.pkl")

#	-----*****-----
#	Changes to the regex pattern because, well, the pdfplumber is not perefect:


leg_name_master.loc[leg_name_master.name == "王定宇", "name_regex"] = "王定[宇孙]"
leg_name_master.loc[leg_name_master.name == "孔文吉", "name_regex"] = "孔文[吉卲]"
leg_name_master.loc[leg_name_master.name == "蔣絜安", "name_regex"] = "蔣絜[孜安]"
leg_name_master.loc[leg_name_master.name == "羅致政", "name_regex"] = "[羅繫]致政"
leg_name_master.loc[leg_name_master.name_indig == "Kolas Yotaka", "name_regex"] = "(谷辣斯[ ．‧]尤達卡|Kolas[ ．‧]{,1}Yotaka)"
#	------*****------ Electric Boogaloo of [宇孙] and [孜安] 
leg_name_master.loc[leg_name_master.name == "趙正宇", "name_regex"] = "趙正[宇孙]"
leg_name_master.loc[leg_name_master.name == "蔣萬安", "name_regex"] = "蔣萬[孜安]"
#	------*****------ More crazy misread
leg_name_master.loc[leg_name_master.name == "施義芳", "name_regex"] = "施[義罬]芳"
leg_name_master.loc[leg_name_master.name_indig == "Kolas Yotaka", "name_regex"] = "(谷辣斯[ ．‧]尤達卡|Kolas[ ．‧]{,1}Y?otaka)"
leg_name_master.loc[leg_name_master.name == "蔣萬安", "name_regex"] = "蔣萬[孜安]"
leg_name_master.loc[leg_name_master.name == "蔣萬安", "name_regex"] = "蔣萬[安孜宊]"
leg_name_master.loc[leg_name_master.name == "高虹安", "name_regex"] = "高虹[安宊]"
leg_name_master.loc[leg_name_master.name == "高虹安", "name_regex"] = "高虹[安宊孜]"
leg_name_master.loc[leg_name_master.name == "陳以信", "name_regex"] = "陳以[信亯]"



#	------*****------ Name change
leg_name_master.loc[leg_name_master.name == "游毓蘭", "name_regex"] = "[游葉]毓蘭"

#	She changed here name from 葉毓蘭 to 游毓蘭, zh.wikipedia.org says 1968年，游毓蘭的生父將她過繼給一位葉姓同事，因此改名為「葉毓蘭」
#	Okay, this is definitely the worst, the pdf is machine-readable EXCEPT when it comes to the name of 



leg_name_master.to_pickle("name_match.pkl")

####  ------******------ WELL, I HAVE TO MANUALLY OVERRIDEN SOME ENTRIES, they are found in the following list of files:
####	/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100109.pdf  
####	陳秀寶 voted nay on proposition (4) and (5) but that his name on the roster was not machine readable, deal with it after all the technical difficulties are dealt with.




####  ------******------ It is amazing that 王定宇's name is rendered as 王定孙, this is madness
####  ------******------ I'll be damned, 孔文吉's name is rendered as 孔文卲, this is madness
####  ------******------ It seems pointless to write down every instances of erroneous reads
####  ------******------ Some incompetent person wrote "Kolas otaka" instead "Kolas Yotaka"	
#	-----*****-----




#	General index assigner (TO DO: Figure out a more efficient way to do it)

def assign_ind(pat_series, txt):
	for i in pat_series.index:
		if re.match(pat_series[i], txt) is not None:
			return i
	return None





def assign_ind_series(pat_series, name_series, val, output):
	count_zero = True
	for name in name_series:
		match = assign_ind(pat_series, name)
		if match is not None:
			output.iat[match] = val
			if count_zero:
				count_zero = False
	if count_zero:
		return 0
	else:
		count = output.value_counts()[val]
		return count







#	Coding guide borrowed from Liao 2022
#	1: yea(from record)
#	2: nay(from record)
#	3: abstain(from record)
#	4: absent(from pdf)
#	5: not serving(from pdf and Legislator_Infos)
#	N.B. Liao's code says 3 is absent and 4 is abstain, this makes coding inconvenient.


	




#	Regex Match

#Note for names, you should probably not use RE.DOTALL, I'll check find names later
def tags(txt):
	return re.findall(ext_search, txt)


def find_names(txt):
	return re.findall(leg_name, txt, re.DOTALL)





#	Meeting Minutes Extraction

def read_minute(txt):
	ind1 = txt.find('\n')
	ind2 = txt.rfind('\n')
	return txt[ind1+1:ind2+1]


def extract_info_lines(pdf):
	info_end = 2
	txts = [ read_minute( pg.extract_text() ) for pg in pdf.pages[:info_end] ]
	return "".join(txts)

#	Meeting Dates Extraction

def convert_roc_gregorian(txt):
	if re.match(ROC_YEAR, txt) is not None:
		roc_year = re.search(ROC_YEAR_NUM, txt).group()
		gregorian_year = roc_year + ROC_YEAR_ZERO
		return re.sub(ROC_YEAR_NUM, "{}年".format(gregorian_year), txt)
	else:
		return txt

def extract_times(pdf):
	txt = extract_info_lines(pdf)
	match = re.search( ROC_TIME_LOC, txt, re.DOTALL)
	if match is None:
		raise Exception("Time information not located")
	time_txt = match.group().replace(' ', '')
	years = re.findall(ROC_YEAR, time_txt)
	if len(years) == 1:
		roc_year = re.search( ROC_YEAR_NUM, years[0]).group()
		gregorian_year = int(roc_year) + ROC_YEAR_ZERO
		date_txts = re.findall(CHN_MMDD_FORMAT, time_txt)	
		date_txts = ["{}年".format(gregorian_year) + date for date in date_txts]
		dates = [datetime.strptime(chn_date, '%Y年%m月%d日') for chn_date in date_txts]
		return dates
	else:
		date_txts = re.findall(ROC_DATE_FORMAT, time_txt)	
		year_num_inds = [   (   ind, re.search(ROC_YEAR_NUM, date).group()  )
							for ind, date in enumerate(date_txts)
								if re.search(ROC_YEAR_NUM, date) is not None ]
		year_num_inds = [(ind, int(year) + ROC_YEAR_ZERO ) for ind, year in year_num_inds]
		date_txts = re.findall(CHN_MMDD_FORMAT, time_txt)	
		end_inds = [element[0] for element in year_num_inds  ][1:]
		end_inds.append(len(date_txts) )
		for i in range(  len(year_num_inds)  ):
			for j in range(year_num_inds[i][0], end_inds[i]):
				date_txts[j] = "{}年".format(year_num_inds[i][1]) + date_txts[j]
		dates = [datetime.strptime(chn_date, '%Y年%m月%d日') for chn_date in date_txts]
		return dates
#	Extracting hour is too much work
#	You get dates only


def extract_leg_presents_lines(pdf):
	txt = extract_info_lines(pdf)
	pattern = "(?<={0}).*?(?={1})".format( LEG_PRESENT_START, LEG_PRESENT_END )
	match = re.search( pattern, txt, re.DOTALL)
	if match is None:
		raise Exception("Time information not located")
	present_txt = match.group()
	present_count = int( re.search(LEG_PRESENT_COUNT, txt).group() )
	present_names = re.findall(ext_search, present_txt)
	if len(present_names) != present_count:
		raise Exception("Your count is wrong")
	return present_names
	


def find_rcv_page(pdf):
	found = None
	for i, pg in enumerate( pdf.pages ):
		if pg.search(RCV_BEGIN):
			return i

def extract_rcv_lines(pdf):
	begin = find_rcv_page(pdf)
	txts = [ read_minute( pg.extract_text() ) for pg in pdf.pages[begin:] ]
	return "".join(txts)


def extract_rcv_txt(pdf):
	txt = extract_rcv_lines(pdf)
	return re.search( "(?<={})".format(RCV_BEGIN) + ".+", txt, re.DOTALL).group()


def extract_rcv_rec_txts(pdf, troubleshoot=False):
	txt = extract_rcv_txt(pdf)
	rec_txts = re.findall(REC_DELIMITERS, txt, flags=re.DOTALL)
	if troubleshoot:
		for ind, rec_txt in enumerate(rec_txts):
			rec_nums = re.findall(title_num, rec_txt)
			if len(rec_nums) == 1:
				if ind + 1 != int(rec_nums[0]):
					raise Exception("The matched rcv has the wrong index!") 
			elif len(rec_nums) == 0:
				raise Exception("Somehow the index of the rcv is not included!")
			else:
				raise Exception("Somehow multiple rcvs are included!")
	return rec_txts

def divide_camp(rec_txt):
	rec_name = re.search(title, rec_txt, re.DOTALL).group()
	rec_votes = re.search(  "{}.+".format(camp) , rec_txt , re.DOTALL  ).group()
	votes = tags(rec_votes)
	start_inds = [ind for ind in range(len(votes)) if re.search(camp, votes[ind]) is not None ]
	ind_count = len(start_inds)
	if ind_count > 3:
		raise Exception("Way too many camps for some reason") 
	elif ind_count < 3:
		raise Exception("Way too few camps for some reason") 
	end_inds = start_inds[1:]
	end_inds.append(len(votes) )
	return rec_name.replace('\n', ''), [votes[start_inds[i]: end_inds[i] ]for i in range(ind_count)  ]
	




def extract_rcv_recs(pdf, troubleshoot=True, troubleshoot_1=False):
	rec_txts = extract_rcv_rec_txts(pdf, troubleshoot)
	return [divide_camp(rec_txt) for rec_txt in rec_txts]


def extract_rcv_recs_1(pdf):
	txt = extract_rcv_txt(pdf)
	recs = tags(txt)
	start_inds = [ind for ind in range(len(recs)) if re.search(title_num, recs[ind]) is not None ]
	rec_nums = len(start_inds)
	end_inds = start_inds[1:]
	end_inds.append(len(recs) )
	return [recs[start_inds[i]: end_inds[i] ]for i in range(rec_nums)  ]


def assign_rcv_votes(rec, output, pat_series):
	name = rec[0]
	flag = 0
	camp_names = rec[1]
	strengths = [int( re.search(camp_strength, camp_names[i][0]).group() ) for i in range( len(rec[1]) ) ]
	yea_count = assign_ind_series(pat_series, camp_names[0][1:], 1, output)
	nay_count = assign_ind_series(pat_series, camp_names[1][1:], 2, output)
	abstain_count = assign_ind_series(pat_series, camp_names[2][1:], 3, output)
	if yea_count != strengths[0]:
		flag += 10
	elif nay_count != strengths[1]:
		flag += 200
	elif abstain_count != strengths[2]:
		flag += 3000
	return [name, output, flag]





def assign_rcv_votes_1(rec, output, pat_series):
	name = rec[0]
	sign_post = [i for i in range(len(rec)) if re.search(camp, rec[i] ) is not None]
	strengths = [int(  re.search(camp_strength, rec[i]).group()  )  for i in sign_post ]
	yea = rec[ sign_post[0]+1 : sign_post[1]  ]
	nay = rec[ sign_post[1]+1 : sign_post[2]  ]
	abstain = rec[ sign_post[2]+1 :  ]
	yea_count = assign_ind_series(pat_series, yea, 1, output)
	nay_count = assign_ind_series(pat_series, nay, 2, output)
	abstain_count = assign_ind_series(pat_series, abstain, 3, output)
	if yea_count != strengths[0]:
		raise Exception("The recorded yea number differ from the minute record")
	elif nay_count != strengths[1]:
		raise Exception("The recorded nay number differ from the minute record")
	elif abstain_count != strengths[2]:
		raise Exception("The recorded abstention number differ from the minute record")
	else:
		return [name, output]



def assign_serving(pdf, output, info_df, pat_series):
	first_page = pdf.pages[0].extract_text()
	term_match = re.search(TERM_NUM,first_page)
	if term_match is None:
		raise Exception("Somehow the header is not correctly read.")
	term = int(  term_match.group()  )
	dates = extract_times(pdf)
	start_date = dates[0]
	end_date = dates[-1]
	elus = info_df[info_df.term == term][ ["name", "onboardDate", "leaveDate"] ]
	assign_ind_series(pat_series, elus.name, 4, output)
	incomplete = elus[  (  elus.onboardDate > elus.onboardDate.min()  )|  (  pd.notnull(elus.leaveDate)  )  ]
	not_serving = incomplete[(incomplete.onboardDate > end_date) | (incomplete.leaveDate < start_date) ]
	assign_ind_series(pat_series, not_serving.name, 5, output)


def add_rcv_rows(pdf, rec_df=None, info_df = legislator_infos, pat_df = leg_name_master ):
	first_page = pdf.pages[0].extract_text()
	meeting_name = re.search("(?<=立法院).+?(?=議事錄)", first_page).group()
	rec_temp = pd.Series(5, index=leg_name_master.index, dtype="int8")
	assign_serving(pdf, rec_temp, info_df, leg_name_master["name_regex"])
	records = extract_rcv_recs(pdf)
	date = extract_times(pdf)[-1]
	rec_full = [assign_rcv_votes(rec, rec_temp.copy(), leg_name_master["name_regex"]) for rec in records]
	rec_raw = pd.DataFrame(  [rec[1] for rec in rec_full]  )	
	test_df = pd.DataFrame( rec_full[0][1]  )
	vote_info = pd.Series(  [rec[0] for rec in rec_full]  )
	flags = pd.Series(  [rec[2] for rec in rec_full]  )
	rec_raw["time"] = date
	rec_raw["meeting_name"] = meeting_name
	rec_raw["title"] = vote_info
	rec_raw["flag"] = flags
	if rec_df is None:
		return rec_raw
	else:
		# There is a future warning that pd.concat will be keyword only, fix it in the future 
		return pd.concat(  [ rec_df, rec_raw ]  )
		





# import required module

# assign directory
directories = ["/Users/williamzhu/Downloads/ly_minute_08",
			"/Users/williamzhu/Downloads/ly_minute_09",
		 	"/Users/williamzhu/Downloads/ly_minute_10"]
	



# iterate over files in
# that directory
rcv_records = [pd.read_pickle(  "./rcv_{:02d}.pkl".format(ind + 8)  ) for ind in range(3)    ] 
irregular = [pd.read_pickle(  "./irregular_rcv_{:02d}.pkl".format(ind + 8)  )  for ind in range(3)    ] 

 








rcv_10_updated = pd.read_pickle(  "./rcv_10_updated.pkl") 
#	Locate the indices of legislators whose votes aren't reflected
missing = leg_name_master[leg_name_master.name.isin(
		["陳秀寳", "傅崐萁"])].index
fu_vote = leg_name_master[leg_name_master.name == "傅崐萁"].index
chen_vote = leg_name_master[leg_name_master.name == "陳秀寳"].index
meeting_indices = rcv_records[-1].meeting_name == "第10屆第1會期第1次會議"
meeting_indices_1 = rcv_records[-1].meeting_name == "第10屆第1會期第9次會議"
title_1 = rcv_records[-1].title.str.contains( "「討論事項第一案嚴重特殊傳染性肺炎防治及紓困振興特別條例委員曾銘宗等提案增訂第九條之三不予通過」部分" )
title_2 = rcv_records[-1].title.str.contains( "「討論事項第一案嚴重特殊傳染性肺炎防治及紓困振興特別條例委員曾銘宗等提案增訂第九條之四不予通過」部分" )

chen = [2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1 ]
fu = [3, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 2]


chen_1 = 2 






#	Manual Override 1
#	In "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100109.pdf"
#	the minutes of 第10屆第1會期第9次會議
#	陳秀寶 is recorded for voting nay on
#	(4)「討論事項第一案嚴重特殊傳染性肺炎防治及紓困振興特別條例委
#	員曾銘宗等提案增訂第九條之三不予通過」部分：
#	and
#	(5)「討論事項第一案嚴重特殊傳染性肺炎防治及紓困振興特別條例委
#	員曾銘宗等提案增訂第九條之四不予通過」部分：
#	but this is not refelected in the dataframe.
#	IT HAS NOT BEEN RESOLVED YET.
#
#	Manual Override 2
#	In "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100101.pdf"
#	the minutes of 第10屆第1會期第1次會議
#	all 12 rcv record contains certain votes
#	that were not captured by pdfplunder
#	They are given in the order of rcvs:
#
#	(1)
#	yea: 
#	nay: 陳秀寶
#	abstain: 傅崐萁
#
#	(2)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(3)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(4)
#	yea:
#	nay: 陳秀寶
#	abstain: 傅崐萁
#
#	(5)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(6)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(7)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(8)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(9)
#	yea: 傅崐萁
#	nay: 陳秀寶
#	abstain:
#
#	(10)
#	yea: 陳秀寶
#	nay: 傅崐萁
#	abstain:
#
#	(11)
#	yea: 陳秀寶
#	nay: 傅崐萁
#	abstain:
#
#	(12)
#	yea: 陳秀寶
#	nay: 傅崐萁
#	abstain:
#
#	No manual override for one flag in "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_09060101.pdf"
#	the minute of 第9屆第6會期第1次臨時會第1次會議
#	(22) 「討論事項第一案外交及國防委員會民進黨黨團新增第 1 案予以
#	通過」部分：
#	the minutes incorrectly recorded that 32 legislators voted nay
#	when only 31 names are on the minutes.
#	Since it is impossible to locate a 32nd legislator who voted nay,
#	the count recorded by minute will be disregarded.

