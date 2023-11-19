
import re

import numpy as np
import pandas as pd



from datetime import datetime

from pathlib import Path

#	Statsmodel stuff, I'm tired, I'm testing the dataset right here
import statsmodels.api as sm
import statsmodels.formula.api as smf





session_pat = "(?<=第)\d+(?=會期)"

def convert_to_pd_int(df):
	int64_cols = df.select_dtypes(include=[ "int8","int64"]).columns
	df.loc[:,int64_cols] = df[int64_cols].astype(  dtype=pd.Int64Dtype()  )


rcv_08 = pd.read_pickle("./rcv_08.pkl")
rcv_09 = pd.read_pickle("./rcv_09.pkl")
rcv_10 = pd.read_pickle(  "./rcv_10_updated.pkl") 
"""
convert_to_pd_int(rcv_08)
convert_to_pd_int(rcv_09)
convert_to_pd_int(rcv_10)
"""

combined = pd.read_pickle("combined_1.pkl")
dpp_2termers = pd.read_pickle("dpp_2termers.pkl")
dpp_two = dpp_2termers.name_id.drop_duplicates()
#print(dpp_2termers.name_id.drop_duplicates() )

dpp_10 = combined[(combined.term == 10) & (combined.party == "民主進步黨" )].drop_duplicates().name_id
dpp_09 = combined[(combined.term == 9) & (combined.party == "民主進步黨" )].drop_duplicates().name_id


#green_910 = [dpp_two] *2
green_910 = [dpp_09, dpp_10]
rcv_910 = [rcv_09, rcv_10]
defections = [[None]*3, [None]*3]

rcvs = [rcv_08, rcv_09, rcv_10]



"""
green_10 = rcv_10.loc[:,dpp_10]
green_10["yea"] = (green_10 == 1).sum(1)
green_10["nay"] = (green_10 == 2).sum(1)
green_10["abstain"] = (green_10 == 3).sum(1)
green_10["absence"] = (green_10 == 4).sum(1)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
	print(green_10[["yea", "nay", "abstain", "absence"]])
"""

input("pause")

def draw_consensus(df):
	df["yea"] = (df == 1).sum(1)
	df["nay"] = (df == 2).sum(1)
	df["abstain"] = (df == 3).sum(1)
	df["absent"] = (df == 4).sum(1)
	df["all_yea"] = ( df.nay == 0) & ( df.abstain == 0 )
	df["all_nay"] = ( df.yea == 0) & ( df.abstain == 0 )
	df["all_abstain"] = ( df.yea == 0) & ( df.nay == 0 )
	df["consensus"] = (df.all_yea) | (df.all_nay) | (df.all_abstain)
	return df.drop(columns=["yea", "nay", "abstain", "absent",\
					 "all_yea", "all_nay", "all_abstain"]\
			)

def count_greens(df, greens):
	df["green_member"] = (df.loc[:,greens] < 5).sum(1) 
	df["green_vote"] = (df.loc[:,greens] < 4).sum(1) 
	df["green_participate"] = (df["green_vote"] > df["green_member"]/3 )
	df["green_yea"] = (df.loc[:,greens] == 1).sum(1)
	df["green_nay"] = (df.loc[:,greens] == 2).sum(1)
	df["green_abstain"] = (df.loc[:,greens] == 3).sum(1)
	df["green_absent"] = (df.loc[:,greens] == 4).sum(1)
	df["dpp_yea"] = (df["green_yea"] > df["green_vote"]/2) & (df["green_participate"])
	df["dpp_nay"] = (df["green_nay"] > df["green_vote"]/2) & (df["green_participate"])
	df["dpp_yea"] = df["dpp_yea"].replace(True, 1).astype( dtype=int)
	df["dpp_nay"] = df["dpp_nay"].replace(True, 2).astype( dtype=int )
	df["dpp_line"] = (df["dpp_yea"]) + (df["dpp_nay"])
	return df.drop(columns=["green_member", "green_vote", "green_participate",\
					"green_yea", "green_nay", "green_abstain", "green_absent",\
					 "dpp_yea", "dpp_nay"]\
			)
	


def green_rcvs(df, greens):
	df = df.reset_index(drop=True)
	df["rcv_index"] = df.index.astype( dtype=pd.Int64Dtype() )
	df = draw_consensus(df)
	df = count_greens(df, greens)
	return df.loc[(df.consensus == False) & (df.dpp_line > 0)].reset_index(drop=True)	

def meeting_defect_rate(df, greens):
	total =  df.groupby(["time"]).apply(lambda x: x[x != 'stranger'].count()  )[greens]
	disloyal = df.groupby(["time"]).apply(lambda x: x[x == 'disloyal'].count()  )[greens]
	print(disloyal/total)
	return disloyal/total

def session_defect_rate(df, greens):
	total =  df.groupby(["session"]).apply(lambda x: x[x != 'stranger'].count()  )[greens]
	disloyal = df.groupby(["session"]).apply(lambda x: x[x == 'disloyal'].count()  )[greens]
	print(disloyal/total)
	return disloyal/total

def term_defect_rate(df, greens):
	total = df[df != 'stranger'].count()[greens]
	disloyal =  df[df == 'disloyal'].count()[greens]
	return disloyal/total

def defect_rate(df, greens, granularity="session"):
	if granularity == "session":
		return session_defect_rate(df, greens)
	elif granularity == "term":
		return term_defect_rate(df, greens)
	elif granularity == "meeting":
		return meeting_defect_rate(df, greens)
	else:
		raise Exception("Granularity incorrectly specified.")
	


def valid_greens(df, greens):
	baseline = df[greens]
	votes =  baseline[baseline < 4].sum()
	return votes[votes > 9].index



def all_session_greens(df, greens, granularity="session"):
	greens = valid_greens(df, greens)
	if granularity == "term":
		return greens
	elif granularity == "session":
		total =  df.groupby(["session"]).apply(lambda x: x[x.isin([1,2,3]) ].count()  )[greens]
		min_attend = total.min()
		return min_attend[min_attend > 0].index
	elif granularity == "meeting":
		total =  df.groupby(["time"]).apply(lambda x: x[x.isin([1,2,3]) ].count()  )[greens]
		min_attend = total.min()
		return min_attend[min_attend > 0].index
	else:
		raise Exception("Granularity incorrectly specified.")
	


def nay_defect(df, greens, granularity="session"):
	df = df.copy()
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == df.dpp_line, "loyal"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x.isin([3,4]), "loyal"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == 5, "stranger"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x.isin([1,2]), "disloyal"),\
							axis=0)
	return defect_rate(df, greens, granularity)

def abstain_defect(df, greens, granularity="session"):
	df = df.copy()
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == df.dpp_line, "loyal"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == 4, "loyal"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == 5, "stranger"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x.isin([1,2,3]), "disloyal"),\
							axis=0)
	return defect_rate(df, greens, granularity)

def absent_defect(df, greens, granularity="session"):
	df = df.copy()
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == df.dpp_line, "loyal"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x == 5, "stranger"),\
							axis=0)
	df[greens] = df[greens].apply(\
							lambda x: x.mask(x.isin([1,2,3,4]), "disloyal"),\
							axis=0)
	return defect_rate(df, greens, granularity)

def defect(df, greens, code, granularity="session"):
	df = df.copy()
	if code == "nay":
		return nay_defect(df, greens, granularity)
	elif code == "abstain":
		return abstain_defect(df, greens, granularity)
	elif code == "absent":
		return absent_defect(df, greens, granularity)


for i,df in enumerate(rcv_910):
	df["session"] = df["meeting_name"].str.extract( "({})".format(session_pat) )  
	df["session"] = df["session"].astype(  dtype=pd.Int64Dtype()  )
	rcv_910[i] = df
	slimmed_greens = green_rcvs(rcv_910[i], green_910[i])
	slimmed_greens = slimmed_greens.reset_index(drop=True)	
	green_910[i] = all_session_greens(slimmed_greens, green_910[i], "term")


best_green = list( set(green_910[0]) & set(green_910[1]) )
best_green_09 = combined[(combined.term == 9) &( combined.name_id.isin(best_green) ) ]
best_green_09 = best_green_09[  ["term", "tier", "name_id"]  ]
best_green_10 = combined[(combined.term == 10) &( combined.name_id.isin(best_green) ) ]
best_green_10 = best_green_10[  ["term", "tier", "name_id"]  ]

stationary_green = pd.merge(best_green_09, best_green_10,
					how="inner",on=["tier","name_id"])
print(best_green)
print(stationary_green.name_id)



"""
input("well, damn")
for i,df in enumerate(rcv_910):
	slimmed_greens = green_rcvs(rcv_910[i], green_910[i])
	slimmed_greens = slimmed_greens.reset_index(drop=True)	
	green_910[i] = all_session_greens(slimmed_greens, green_910[i])
	for j, option in  enumerate(["nay", "abstain", "absent"]):
		rebels = defect(slimmed_greens, green_910[i], option, "term" ).T
		#rebels = defect(slimmed_greens, green_910[i], option).T
		rebels = rebels.reset_index().rename(columns={"index": "name_id", 0:"defect_rate"})
		rebels = rebels.rename_axis(None, axis=1)
		print(rebels)
		defections[i][j] = rebels
	#print(slimmed_greens)


leg_09 = combined[combined.term == 9]
leg_10 = combined[combined.term == 10]
for j in range( len( defections[0]  )   ): 
	defection_09 = defections[0][j]
	defection_10 = defections[1][j]
	defection_09 = defection_09.merge(leg_09, how = "left", on="name_id")
	defection_10 = defection_10.merge(leg_10, how = "left", on="name_id")
	defection_910 = pd.concat([defection_09, defection_10])
	defection_910.to_csv("defection_by_term_type_{}.csv".format(j+1) )
"""




"""
test_09 = defections[0][0]

test_10 = defections[1][0]
leg_09 = combined[combined.term == 9]
leg_10 = combined[combined.term == 10]
test_09 = test_09.merge(leg_09, how = "left", on="name_id")
test_10 = test_10.merge(leg_10, how = "left", on="name_id")
test_910 = pd.concat([test_09, test_10])
print(test_910)
test_910.to_csv("test_910_2.csv")
"""
#test = test.merge(leg_10, how="left", on="name_id")
#print(test)
#print(test.columns)
#test.to_csv("test.csv")

#	-----******----- Below are examples of how you handle sessions
#test = defections[1][2]
#test = test.drop_duplicates()
#test = test[test.iloc[1:6].notnull() ]
#test = test[test.iloc[:,1:7].notnull().all(1)]
#test.columns = test.columns.astype(str)
#test = test.melt(id_vars=['name_id'], value_vars=['1', '2', '3', '4', '5', '6'],
#        var_name='session', value_name='defect_rate')
#test.session = test.session.astype(int)
#print(test)
#input("examine melt result")


#leg_10 = combined[combined.term == 10]


#test = test.merge(leg_10, how="left", on="name_id")
#print(test)
#print(test.columns)
#test.to_csv("test.csv")

"""
for i in range(len(rcvs) ):
	rcvs[i]["session"] = rcvs[i]["meeting_name"].str.extract( "({})".format(session_pat) )  
	rcvs[i]["session"] = rcvs[i]["session"].astype(  dtype=pd.Int64Dtype()  )

#rcv_10.reset_index()

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
	print(rcv_10)
	print(rcv_08[["time", "session"]].sort_values("time"))
	print(rcv_09[["time", "session"]].sort_values("time"))
	print(rcv_10[["time", "session"]].sort_values("time"))
"""


for i,df in enumerate(rcv_910):
	slimmed_greens = green_rcvs(rcv_910[i], green_910[i])
	slimmed_greens = slimmed_greens.reset_index(drop=True)	
	green_910[i] = all_session_greens(slimmed_greens, green_910[i])
	for j, option in  enumerate(["nay", "abstain", "absent"]):
		#rebels = defect(slimmed_greens, green_910[i], option, "term" ).T
		rebels = defect(slimmed_greens, green_910[i], option).T
		rebels = rebels.reset_index().rename(columns={"index": "name_id", 0:"defect_rate"})
		rebels = rebels.rename_axis(None, axis=1)
		rebels.columns = rebels.columns.astype(str)
		print(rebels.columns[1:])
		test = rebels.melt(id_vars=['name_id'], value_vars= rebels.columns[1:],
    	    var_name='session', value_name='defect_rate')
		test["session"] = test["session"].astype(  dtype=pd.Int64Dtype()  )
		print(test.dtypes)
		#input("oh my")
		#defections[i][j] = rebels
		defections[i][j] = test
	#print(slimmed_greens)


leg_09 = combined[combined.term == 9]
leg_10 = combined[combined.term == 10]
for j in range( len( defections[0]  )   ): 
	defection_09 = defections[0][j]
	defection_10 = defections[1][j]
	defection_09 = defection_09.merge(leg_09, how = "left", on="name_id")
	defection_10 = defection_10.merge(leg_10, how = "left", on="name_id")
	defection_910 = pd.concat([defection_09, defection_10])
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
		print(defection_910)
		input("uh oh")
	defection_910.to_csv("defection_by_session_type_{}.csv".format(j+1) )

"""



for i,df in enumerate(rcv_910):
	slimmed_greens = green_rcvs(rcv_910[i], green_910[i])
	slimmed_greens = slimmed_greens.reset_index(drop=True)	
	green_910[i] = all_session_greens(slimmed_greens, green_910[i])
	for j, option in  enumerate(["nay", "abstain", "absent"]):
		rebels = defect(slimmed_greens, green_910[i], option, "meeting" ).T
		#rebels = defect(slimmed_greens, green_910[i], option).T
		rebels = rebels.reset_index().rename(columns={"index": "name_id", 0:"defect_rate"})
		rebels = rebels.rename_axis(None, axis=1)
		#rebels.columns = rebels.columns.astype(str)
		print(rebels.columns[1:])
		test = rebels.melt(id_vars=['name_id'], value_vars= rebels.columns[1:],
    	    var_name='time', value_name='defect_rate')
		#test["session"] = test["session"].astype(  dtype=pd.Int64Dtype()  )
		print(test.dtypes)
		#input("oh my")
		#defections[i][j] = rebels
		defections[i][j] = test
	#print(slimmed_greens)


leg_09 = combined[combined.term == 9]
leg_10 = combined[combined.term == 10]
for j in range( len( defections[0]  )   ): 
	defection_09 = defections[0][j]
	defection_10 = defections[1][j]
	defection_09 = defection_09.merge(leg_09, how = "left", on="name_id")
	defection_10 = defection_10.merge(leg_10, how = "left", on="name_id")
	defection_910 = pd.concat([defection_09, defection_10])
	defection_910.to_csv("defection_by_time_type_{}.csv".format(j+1) )


"""
