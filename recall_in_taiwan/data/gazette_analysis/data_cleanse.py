


from pathlib import Path

import datetime
import re

import numpy as np
import pandas as pd
import minute_parse

missing_cols = ['birth_date', 'age', 'place_of_birth',
       'degree', 'incumbent', 'valid_votes', 'total_votes', 'electorate',
       'pop', 'electorate_over_pop_pct', 'total_votes_over_electorate_pct',
       'elected_over_cands_pct', 'vote', 'vote_over_total_votes_pct',
       'vote_margin', 'vote_over_total_votes_pct_margin']

def convert_to_pd_int(df):
	int64_cols = df.select_dtypes(include=["int64"]).columns
	df.loc[:,int64_cols] = df[int64_cols].astype(  dtype=pd.Int64Dtype()  )

def fill_df(df, term, name, arr, colnames = missing_cols):
	df.loc[ (df.term == term) & (df.name_x == name) & (df.vote.isnull()  ), colnames ] = arr
	print( df.loc[ (df.term == term) & (df.name_x == name) & (df.vote.isnull()  ), colnames ] )



def fill_df_dict(df, term, row_dict, colnames = missing_cols):
	names = df.loc[ (df.term == term) &(df.tier == 1) & (df.vote.isnull()  ) ].name_x
	print(names)
	for name in names:
		fill_df( df, term, name, row_dict[name], colnames)

def percentage(num, denom):
	quotient = num/denom
	precision = 4
	figure = round(quotient, precision)
	return figure * 100



def handle_turnout(valid, total, electorate, population):
	part_1 = [valid, total, electorate, population]
	part_2 = [percentage(electorate,population), percentage(total, population) ]
	return part_1 + part_2

def handle_outcome(winner, runner_up, valid):
	part_1 = [winner, percentage(winner, valid)]
	margin = winner - runner_up
	part_2 = [margin, percentage(margin, valid)]
	return part_1 + part_2

"""
missing_林靜儀 = [datetime.datetime(1974, 2, 12), 47,"臺灣省",
				6, 2, 171251, 172446, 295985,
				365586, round(295985/365586, 4 )*100, round(172446/295985, 4 )*100,
				round(20.00, 2), 88752, round(88752/171251, 4)*100,
				88752-80912, round( (88752-80912)/171251, 4)*100 ]
"""
# Import the beautifulsoup
# and request libraries of python.




#	------*****----- Import combined_electoral_return
electoral_returns = "combined_electoral_return_{}.pkl"
combined_electoral_return = [ pd.read_pickle(electoral_returns.format(2012 + i*4)) for i in range(3)]


#	------*****----- Slim down combined_electoral_return

to_remove = ["prov_metro", "county", "district", "ballot_num_x",
			"name_y", "party_id", "sex_y", "elected_x",
			"ballot_num_y", "elected_y"]	
to_remove_1 = ["ename", "party_y", "invalid_votes"]
for ind, electoral_return in enumerate(combined_electoral_return):
	print(combined_electoral_return[ind].shape)
	combined_electoral_return[ind] = electoral_return.drop(columns=to_remove)
	combined_electoral_return[ind] = combined_electoral_return[ind].drop(columns=to_remove_1)
	print(combined_electoral_return[ind].shape)

constituency_dict = {"全國不分區及僑居國外國民": 2,
					"平地原住民": 3,
					"..[市縣]\d{,2}": 1,
					"山地原住民": 4}


for vote_return in combined_electoral_return:
	area_abbr = vote_return.areaName.str.replace("選舉區", '')
	area_abbr = area_abbr.str.replace("第", '')
	area_abbr = area_abbr.str.replace("台", '臺')
	vote_return["constituency"] = area_abbr



with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	for electoral_return in combined_electoral_return:
		replaced = electoral_return.replace({"constituency": constituency_dict}, regex=True)
		electoral_return[  ["tier"]  ] = replaced[  ["constituency"]  ].astype(  dtype=pd.Int64Dtype()  )



for vote_return in combined_electoral_return:
	print(vote_return[  (  vote_return.vote.isnull()  ) & (vote_return.tier == 1)  ].name_x)




missing_林靜儀 = [datetime.datetime(1974, 2, 12), 47,"臺灣省",
				6, 2, 171251, 172446, 295985,
				365586, round(295985/365586, 4 )*100, round(172446/295985, 4 )*100,
				round(20.00, 2), 88752, round(88752/171251, 4)*100,
				88752-80912, round( (88752-80912)/171251, 4)*100 ]
missing_王鴻薇 = [datetime.datetime(1964, 7, 10), 58,"臺灣省",
				4, 2, 115800, 116155, 267965,
				350793, round(267965/350793, 4 )*100, round(116155/267965, 4 )*100,
				round(33.33, 2), 60519, round(60519/115800, 4)*100,
				60519 - 54739, round( (60519-54739)/115800, 4)*100 ]

row_dict_2020 = { "林靜儀": missing_林靜儀,
				"王鴻薇": missing_王鴻薇}


"""
"""
missing_何志偉 = [datetime.datetime(1982, 5, 14), 36,"臺北市", 5, 2] +\
				handle_turnout(80798, 81107, 266907, 342977) +\
				[round(20.00, 2)] +\
				handle_outcome(38591, 31532, 80798)
missing_余天 = [datetime.datetime(1948, 3, 1), 71,"臺灣省", 2, 2] +\
				handle_turnout(109318, 109939, 261154, 347738) +\
				[round(33.33, 2)] +\
				handle_outcome(56888, 51127, 109318)
missing_柯呈枋 = [datetime.datetime(1972, 11, 30), 46,"臺灣省", 5, 2] +\
				handle_turnout(91803, 92411, 252529, 316271) +\
				[round(33.33, 2)] +\
				handle_outcome(47835, 41946, 91803)
missing_沈智慧 = [datetime.datetime(1957, 9, 16), 61,"臺中市", 6, 2] +\
				handle_turnout(85200, 85621, 337848, 408518) +\
				[round(25.00, 2)] +\
				handle_outcome(49230, 32903, 85200)
missing_郭國文 = [datetime.datetime(1967, 3, 11), 52,"臺南市", 6, 2] +\
				handle_turnout(133587, 134275, 301571, 364580) +\
				[round(16.67, 2)] +\
				handle_outcome(62858, 59194, 133587)
missing_陳玉珍 = [datetime.datetime(1973, 10, 29), 45,"金馬地區", 5, 2] +\
				handle_turnout(24803, 24968, 117730, 131568) +\
				[round(16.67, 2)] +\
				handle_outcome(7117, 6020, 24803)
row_dict_2016 = {"何志偉": missing_何志偉,
				"余天": missing_余天,
				"柯呈枋": missing_柯呈枋,
				"沈智慧": missing_沈智慧,
				"郭國文": missing_郭國文,
				"陳玉珍": missing_陳玉珍}
				


missing_徐志榮 = [datetime.datetime(1955, 7, 31), 59,"臺灣省", 2, 2] +\
				handle_turnout(80922, 81430, 231684, 289714) +\
				[round(33.33, 2)] +\
				handle_outcome(47105, 32966, 80922)

missing_莊瑞雄 = [datetime.datetime(1963, 4, 20), 51,"臺灣省", 5, 2] +\
				handle_turnout(65256, 65570, 202129, 256898) +\
				[round(25.00, 2)] +\
				handle_outcome(43988, 20627, 65256)

missing_許淑華 = [datetime.datetime(1975, 10, 15), 39,"臺灣省", 5, 2] +\
				handle_turnout(75692, 76132, 205390, 258867) +\
				[round(33.33, 2)] +\
				handle_outcome(38694, 34938, 75692)

missing_陳素月 = [datetime.datetime(1966, 1, 18), 49,"臺灣省", 5, 2] +\
				handle_turnout(96831, 97597, 259816, 332584) +\
				[round(20.00, 2)] +\
				handle_outcome(51907, 34707, 96831)

missing_顏寬恒 = [datetime.datetime(1977, 9, 14), 35,"臺中市", 5, 2] +\
				handle_turnout(133059, 134500, 275086, 356694) +\
				[round(33.33, 2)] +\
				handle_outcome(66457, 65319, 133059)

missing_黃國書 = [datetime.datetime(1964, 1, 3), 51,"臺灣省", 5, 2] +\
				handle_turnout(78060, 78495, 255203, 325947) +\
				[round(50.00, 2)] +\
				handle_outcome(45143, 32917, 78060)


row_dict_2012 = {"徐志榮": missing_徐志榮,
	"莊瑞雄": missing_莊瑞雄,
	"許淑華": missing_許淑華,
	"陳素月": missing_陳素月,
	"顏寬恒": missing_顏寬恒,
	"黃國書": missing_黃國書}



fill_df_dict(combined_electoral_return[0], 8, row_dict_2012)
fill_df_dict(combined_electoral_return[1], 9, row_dict_2016)
fill_df_dict(combined_electoral_return[-1], 10, row_dict_2020)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	print(combined_electoral_return[0][ (combined_electoral_return[0].tier == 2)])# & (combined_electoral_return[0].vote.isnull()  ) ]   )
	print(combined_electoral_return[1][ (combined_electoral_return[1].tier == 2)])# & (combined_electoral_return[1].vote.isnull()  ) ]   )
	print(combined_electoral_return[-1][ (combined_electoral_return[-1].tier == 2)])# & (combined_electoral_return[-1].vote.isnull()  ) ]   )
for i in range( len(combined_electoral_return) ):
	combined_electoral_return[i].columns = combined_electoral_return[i].columns.str.removesuffix("_x")
	print(combined_electoral_return[i].columns)
	input("Pause to examine.")
	combined_electoral_return[i].to_pickle("cleaned_bio_{}.pkl".format(2012 + i*4)  )



