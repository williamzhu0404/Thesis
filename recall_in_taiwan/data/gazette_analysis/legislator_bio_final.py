

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
	#if output.shape[0] != df2_nrow:
		#print(output.shape[0], df2_nrow)
	#else:
		#print("IT'S A FULL MATCH!")
	return output

def convert_to_pd_int(df):
	int64_cols = df.select_dtypes(include=[ "int64"]).columns
	df.loc[:,int64_cols] = df[int64_cols].astype(  dtype=pd.Int64Dtype()  )

def add_defect_row(row, info_dict):
	pass


print(indexed_leg_infos.dtypes)
"""
input("check leg_infos dtypes")
name_id                 Int64
term                    Int64
name                   object
ename                  object
sex                     Int64
party                  object
partyGroup             object
areaName               object
onboardDate    datetime64[ns]
leaveFlag              object
leaveDate      datetime64[ns]
leaveReason            object


>>> combined.columns
Index(['name_id', 'term', 'name', 'sex', 'party', 'partyGroup', 'areaName',
       'onboardDate', 'leaveFlag', 'leaveDate', 'leaveReason', 'party_num',
       'party_group_num', 'birth_date', 'age', 'place_of_birth', 'degree',
       'incumbent', 'valid_votes', 'total_votes', 'electorate', 'pop',
       'electorate_over_pop_pct', 'total_votes_over_electorate_pct',
       'elected_over_cands_pct', 'vote', 'vote_over_total_votes_pct',
       'vote_margin', 'vote_over_total_votes_pct_margin', 'constituency',
       'tier', 'lnpopudensity'],
"""


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
print(suspects.columns)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	print(suspects)
"""
    name  name_id  flag
0    孫大千       37     2
1    徐欣瑩       61     2
2    徐耀昌       63     2
3    李慶華       78     2
4    李桐豪       82     2
5    林世嘉       87     2
6    林德福       95     2
7    林郁方      107     2
8    蘇震清      193     2
9    謝國樑      202     2
10   陳雪生      271     2
11  高金素梅      281     2
12   黃國書      289     2
13   林昶佐       99     2
14   林為洲      105     2
15   洪慈庸      132     2
16   陳玉珍      259     2
17   傅崐萁        8     2
"""
input("Examine suspects.")

#	-----******----- investigation outcome:
"""
256        8    10  傅崐萁    1  中國國民黨      中國國民黨    花蓮縣選舉區  2020-02-01   
22        61     8  徐欣瑩    2    民國黨      立院新聯盟    新竹縣選舉區  2012-02-01   
164       99     9  林昶佐    1    無黨籍         0無  臺北市第5選舉區  2016-02-01   
288       99    10  林昶佐    1    無黨籍         0無  臺北市第5選舉區  2020-02-01   
179      132     9  洪慈庸    2    無黨籍         0無  臺中市第3選舉區  2016-02-01   
80       193     8  蘇震清    1  民主進步黨      民主進步黨  屏東縣第1選舉區  2012-02-01   
204      193     9  蘇震清    1  民主進步黨      民主進步黨  屏東縣第1選舉區  2016-02-01   
325      193    10  蘇震清    1    無黨籍      民主進步黨  屏東縣第2選舉區  2020-02-01   
234      259     9  陳玉珍    2  中國國民黨      中國國民黨    金門縣選舉區  2019-03-21   
355      259    10  陳玉珍    2  中國國民黨      中國國民黨    金門縣選舉區  2020-02-01   
112      271     8  陳雪生    1  中國國民黨      中國國民黨    連江縣選舉區  2012-02-01   
239      271     9  陳雪生    1  中國國民黨      中國國民黨    連江縣選舉區  2016-02-01   
361      271    10  陳雪生    1  中國國民黨      中國國民黨    連江縣選舉區  2020-02-01   
120      289     8  黃國書    1  民主進步黨      民主進步黨  台中市第6選舉區  2015-02-16   
249      289     9  黃國書    1  民主進步黨      民主進步黨  臺中市第6選舉區  2016-02-01   
369      289    10  黃國書    1    無黨籍         0無  臺中市第6選舉區  2020-02-01   
"""


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
"""
   name  name_id  flag  defect_term
17  傅崐萁        8     2           10
1   徐欣瑩       61     2            8
13  林昶佐       99     2            9
15  洪慈庸      132     2            9
8   蘇震清      193     2           10
16  陳玉珍      259     2            9
10  陳雪生      271     2            8
12  黃國書      289     2           10
"""
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
"""
   name  name_id  flag  defect_term defect_date
17  傅崐萁        8     2           10  2021-11-19
1   徐欣瑩       61     2            8  2015-02-12
13  林昶佐       99     2            9  2019-08-01
15  洪慈庸      132     2            9  2019-08-13
8   蘇震清      193     2           10  2021-02-26
16  陳玉珍      259     2            9  2019-08-14
10  陳雪生      271     2            8  2015-07-08
12  黃國書      289     2           10  2021-10-17
"""


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
print(combined.shape)
print(combined.columns)
combined = pd.concat(  [combined, defection])
print(combined.shape)
print(combined.columns)

"""
     name_id  term name  sex  party partyGroup  areaName onboardDate  \
22        61     8  徐欣瑩    2    民國黨      立院新聯盟    新竹縣選舉區  2012-02-01   
112      271     8  陳雪生    1  中國國民黨      中國國民黨    連江縣選舉區  2012-02-01   
164       99     9  林昶佐    1    無黨籍         0無  臺北市第5選舉區  2016-02-01   
179      132     9  洪慈庸    2    無黨籍         0無  臺中市第3選舉區  2016-02-01   
234      259     9  陳玉珍    2  中國國民黨      中國國民黨    金門縣選舉區  2019-03-21   
256        8    10  傅崐萁    1  中國國民黨      中國國民黨    花蓮縣選舉區  2020-02-01   
325      193    10  蘇震清    1    無黨籍      民主進步黨  屏東縣第2選舉區  2020-02-01   
369      289    10  黃國書    1    無黨籍         0無  臺中市第6選舉區  2020-02-01   
  leaveFlag leaveDate leaveReason  party_num  party_group_num birth_date  \
22          否       NaT         NaN        999              999 1972-04-23   
112         否       NaT         NaN          1                1 1952-01-01   
164         否       NaT         NaN        999              999 1976-02-01   
179         否       NaT         NaN        999              999 1982-12-20   
234         否       NaT         NaN          1                1 1973-10-29   
256         否       NaT         NaN          1                1 1962-05-08   
325         否       NaT         NaN        999               16 1965-02-02   
369         否       NaT         NaN        999              999 1964-01-03   
"""

"""
    name_id  term name  sex  party partyGroup      areaName onboardDate  ... vote_margin vote_over_total_votes_pct_margin  constituency tier lnpopudensity experience  defect_date defect_period
52      134     8  洪秀柱    2  中國國民黨      中國國民黨  全國不分區及僑居國外國民  2012-02-01  ...        <NA>                              NaN  全國不分區及僑居國外國民    2           NaN          6          NaT          <NA>
59      151     8  王金平    1  中國國民黨      中國國民黨  全國不分區及僑居國外國民  2012-02-01  ...        <NA>                              NaN  全國不分區及僑居國外國民    2           NaN          6          NaT          <NA>
72      173     8  蔡其昌    1  民主進步黨      民主進步黨      台中市第1選舉區  2012-02-01  ...       16231                            10.84          臺中市1    1      6.952317          1          NaT          <NA>
184     151     9  王金平    1  中國國民黨      中國國民黨  全國不分區及僑居國外國民  2016-02-01  ...        <NA>                              NaN  全國不分區及僑居國外國民    2           NaN          7          NaT          <NA>
193     173     9  蔡其昌    1  民主進步黨      民主進步黨      臺中市第1選舉區  2016-02-01  ...       31062                            22.14          臺中市1    1      6.952317          2          NaT          <NA>
201     189     9  蘇嘉全    1  民主進步黨      民主進步黨  全國不分區及僑居國外國民  2016-02-01  ...        <NA>                              NaN  全國不分區及僑居國外國民    2           NaN          2          NaT          <NA>
302     137    10  游錫堃    1  民主進步黨      民主進步黨  全國不分區及僑居國外國民  2020-02-01  ...        <NA>                              NaN  全國不分區及僑居國外國民    2           NaN          0          NaT          <NA>
318     173    10  蔡其昌    1  民主進步黨      民主進步黨      臺中市第1選舉區  2020-02-01  ...       59326                            37.19          臺中市1    1      6.949502          3          NaT 
"""
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
input("hang on")



with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	print(dpp_2termers)
	#print(combined[ combined.defect_date.notnull() ] )
	#print(combined[["president"]])
	#print(combined.dtypes)






















