

from pathlib import Path


import datetime
import re

import numpy as np
import pandas as pd


NO_PARTY = 999
ROC_YEAR_ZERO = 1911


leg_name_master = pd.read_pickle("leg_name_remastered.pkl")
investigate = pd.read_pickle("flag.pkl")
combined = pd.read_pickle("combined.pkl")
indexed_paper_data = pd.read_pickle("indexed_paper_data.pkl")
indexed_leg_infos = pd.read_pickle("indexed_leg_info.pkl")

def merge_regex(df1, df2):
	df2_nrow = df2.shape[0]
	idx = [(i,j) for i,r in enumerate(df1.name_regex) for j,v in enumerate(df2.name) if re.match(r,v)]
	df1_idx, df2_idx = zip(*idx)
	t = df1.iloc[list(df1_idx),-1].reset_index(drop=True)
	t1 = df2.iloc[list(df2_idx),:].reset_index(drop=True)
	output = pd.concat([t,t1],axis=1)
	return output

def convert_to_pd_int(df):
	int64_cols = df.select_dtypes(include=[ "int64"]).columns
	df.loc[:,int64_cols] = df[int64_cols].astype(  dtype=pd.Int64Dtype()  )



#	-----*****-----	Experience operationalized as the number of terms rounded up minus 1
indexed_leg_infos["experience"] = indexed_leg_infos.groupby("name_id")["term"].rank(method="dense", ascending=True) - 1
indexed_leg_infos["experience"] = indexed_leg_infos["experience"].astype(  dtype=pd.Int64Dtype()  )

combined = combined.merge(indexed_leg_infos[["name_id", "term", "experience"]],
							how="left", on=["name_id","term"])

suspects = pd.concat([leg_name_master[ ["name", "name_id"]], investigate], axis=1)  
suspects.columns.values[-1] = "flag"
suspects = suspects[suspects.iloc[:, -1] == 2]
suspects = pd.merge(combined[ ["name", "name_id"]].drop_duplicates() ,
					suspects[  ["name_id", "flag"]  ] ,
					how="inner", on="name_id")


defectors = suspects.copy()
innocent = [37,
			63,
			78,
			82,
			87,
			95,
			107,
			202,
			281,
			105]
defectors.loc[defectors.name_id.isin(innocent), "flag"] = 1
defectors = defectors[defectors.iloc[:, -1] == 2]
defectors = defectors.sort_values("name_id")
defectors["term"] = [ 10,
							8,
							9,
							9,
							10,
							9,
							8,
							10]
defectors["term"] = defectors["term"].astype(  dtype=pd.Int64Dtype()  )
defectors["defect_date"] = [ datetime.datetime(2021, 11, 19),
							 datetime.datetime(2015, 2, 12),
							 datetime.datetime(2019, 8, 1),
							 datetime.datetime(2019, 8, 13),
							 datetime.datetime(2021, 2, 26),
							 datetime.datetime(2019, 8, 14),
							 datetime.datetime(2015, 7, 8),
							 datetime.datetime(2021, 10, 17)]
defectors["defect_period"] = 2
defectors["defect_period"] = defectors["defect_period"].astype(  dtype=pd.Int64Dtype()  )


defect_傅崐萁 = {\
				"name_id": 8,
				"party": "無黨籍", 
				"partyGroup": "0無", 
				"party_num": 999, 
				"party_group_num": 999}

defect_徐欣瑩 = {\
				"name_id": 61,
				"party": "中國國民黨",
				"partyGroup": "中國國民黨", 
				"party_num": 1, 
				"party_group_num": 1}


defect_林昶佐 = {\
				"name_id": 99,
				"party": "時代力量", 
				"partyGroup": "時代力量", 
				"party_num": 267, 
				"party_group_num": 267}


defect_洪慈庸 = {\
				"name_id": 132,
				"party": "時代力量", 
				"partyGroup": "時代力量", 
				"party_num": 267, 
				"party_group_num": 267}


defect_蘇震清 = {\
				"name_id": 193,
				"party": "民主進步黨", 
				"partyGroup": "民主進步黨", 
				"party_num": 16, 
				"party_group_num": 16}


defect_陳玉珍 = {\
				"name_id": 259,
				"party": "無黨籍", 
				"partyGroup": "中國國民黨", 
				"party_num": 999, 
				"party_group_num": 1}


defect_陳雪生 = {\
				"name_id": 271,
				"party": "無黨籍", 
				"partyGroup": "0無", 
				"party_num": 999, 
				"party_group_num": 999}

defect_黃國書 = {\
				"name_id": 289,
				"party": "民主進步黨", 
				"partyGroup": "民主進步黨", 
				"party_num": 16, 
				"party_group_num": 16}

before = [defect_傅崐萁,
defect_徐欣瑩,
defect_林昶佐,
defect_洪慈庸,
defect_蘇震清,
defect_陳玉珍,
defect_陳雪生,
defect_黃國書]


before_df = pd.concat( [pd.DataFrame(info, index=[ind] ) for ind, info in enumerate(before)], axis=0 )


combined = combined.merge(defectors[\
		 ["name_id", "term", "defect_date", "defect_period"]\
		], how="left",\
		left_on=[ "name_id", "term"],\
		right_on=[ "name_id", "term"])


defection = combined[combined.defect_date.notnull()  ]  
defection = defection.sort_values("name_id").reset_index(drop=True)
before_df = before_df.sort_values("name_id").reset_index(drop=True)
defection.update(before_df)
defection["defect_period"] = 1
defection["defect_period"] = defection["defect_period"].astype(  dtype=pd.Int64Dtype()  )
combined = pd.concat(  [combined, defection])

leg_prez = {"term": [8, 9, 10],
			"name_id":[151, 189, 137],
			"president":[1, 1, 1]}
leg_prez = pd.DataFrame(leg_prez).astype(  dtype=pd.Int64Dtype()  )
leg_veep = {"term": [8, 9, 10],
			"name_id":[134, 173, 173],
			"vice_president":[1, 1, 1]}
leg_prez = pd.DataFrame(leg_prez).astype(  dtype=pd.Int64Dtype()  )
leg_veep = pd.DataFrame(leg_veep).astype(  dtype=pd.Int64Dtype()  )
		
combined = combined.merge( leg_prez, how="left", on=["term", "name_id"])
combined = combined.merge( leg_veep, how="left", on=["term", "name_id"])
combined[["president"]] = combined[["president"]].fillna(0)
combined[["vice_president"]] = combined[["vice_president"]].fillna(0)


leg_910_dpp = combined[(combined.term > 8) & ( combined.party == "民主進步黨") ]

two_termers = leg_910_dpp[ ["name_id", "term"] ].drop_duplicates()
two_termers = two_termers.groupby("name_id").count()
two_termers = two_termers[two_termers.term > 1].index
dpp_2termers = leg_910_dpp[leg_910_dpp.name_id.isin( two_termers) ]
dpp_2termers = dpp_2termers[dpp_2termers.president != 1]
dpp_2termers = dpp_2termers[dpp_2termers.vice_president != 1]
dpp_2termers.to_pickle("dpp_2termers.pkl")
combined.to_pickle("combined_1.pkl")






