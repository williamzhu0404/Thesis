
from pathlib import Path

import datetime
import re

import numpy as np
import pandas as pd
import minute_parse

def convert_to_pd_int(df):
	int64_cols = df.select_dtypes(include=["int64"]).columns
	df.loc[:,int64_cols] = df[int64_cols].astype(  dtype=pd.Int64Dtype()  )

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




# Import the beautifulsoup
# and request libraries of python.



leg_name_master = pd.read_pickle("leg_name_remastered.pkl")
investigate = pd.read_pickle("flag.pkl")
#Legislator_Infos = pd.read_csv("16_CSV_16_CSV.csv")




paper_data = pd.read_csv("paper_data.csv")
#leg_7_10 = Legislator_Infos[Legislator_Infos.term > 6]


#indexed_paper_districted = 






#	------*****----- Import cleaned_bios
cleaned_bio = "cleaned_bio_{}.pkl"
cleaned_bios = [ pd.read_pickle(cleaned_bio.format(2012 + i*4)  ) for i in range(3)]
#print(cleaned_bios[0].columns)


#	------*****------	SPECIAL HANDLING FOR 桃園縣 elevation to 直轄市
for i in range( len(cleaned_bios) -1):
	cleaned_bios[i]["constit"] = cleaned_bios[i]["constituency"].str.replace("桃園[縣市]", '桃園', regex=True)



int64_cols = [0] + [i for i in range(2, 25)] +\
			 [i for i in range(27, 39)] +\
			 [i for i in range(42, 45)] +\
			 [i for i in range(50, 52)] +\
			 [i for i in range(53, 63)]
paper_data.iloc[:, int64_cols] = paper_data.iloc[:, int64_cols].astype(  dtype=pd.Int64Dtype()  )



#convert_to_pd_int(paper_data)
indexed_paper_data = merge_regex(leg_name_master.iloc[:, -2:], paper_data)


print(indexed_paper_data.shape)
indexed_paper_data = indexed_paper_data.merge(\
					pd.concat([cleaned_bios[i]for i in range(2)])\
					[ ["name_id", "term", "constit" ]  ],\
					how="left", left_on =["order", "name_id"],\
					right_on=["term", "name_id"])
print(indexed_paper_data.shape)
indexed_paper_data.to_pickle("indexed_paper_data.pkl")




print("You are reading the reindexed paper data.")
"""
Index(['name_id', 'order', 'name', 'mpid', 'party', 'edu', 'gender',
       'category', 'bir_year', 'term', 'vote_get', 'vote_rate', 'con_size',
       'lre', 'lgo', 'lchief', 'pfa', 'cre', 'govmember', 'partyswitch',
       'leave', 'newcomer', 'faction', 'personid', 'chair', 'termsquare',
       'termlog', 'termlog10', 'tier3', 'dtier31', 'dtier32', 'dtier33',
       'tier2', 'dtier21', 'dtier22', 'reform', 'csm', 'party4', 'csm2',
       'edu3', 'deviall', 'abstain', 'against', 'caseid', 'age', 'chairtime',
       'deviall2', 'abstain2', 'against2', 'lnpopudensity', 'pupdensity_new',
       'lcpolitics', 'lcpolitics2', 'absence', 'tier2n', 'dtier2n1',
       'dtier2n2', 'sntv', 'sntvlowdm', 'sntvhighdm', 'aboriginal',
       'pluralitysmd', 'prlinked', 'prindep', 'elecsecurity', 'lndm'],
      dtype='object')
"""

extended = [None] * 3
const_info = indexed_paper_data.loc\
				[ (indexed_paper_data.order == 8) &\
				(indexed_paper_data.dtier31 == 1),\
				["constit", "lnpopudensity"]]
const_info = const_info.drop_duplicates()
for i in range(  len(extended) -1 ):
	print(cleaned_bios[i].shape)
	extended[i] = pd.merge\
				(cleaned_bios[i], const_info,\
				how="left", on="constit")
	#with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
		#print(extended[i])
	print(extended[i].shape)
	print(cleaned_bios[i].shape[0] == extended[i].shape[0])
	extended[i] = extended[i].drop(columns=["constit"] ) 
	print(extended[i].shape)
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
		print(extended[i].sort_values("constituency")  )
	input("Let us slow down")
# constituency info from paper data



# constituency info from outside
"""
constituency_wikipedia_link = "https://zh.wikipedia.org/zh-hant/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E7%AB%8B%E6%B3%95%E5%A7%94%E5%93%A1%E9%81%B8%E8%88%89%E5%8D%80%E5%88%97%E8%A1%A8"
tables = pd.read_html(constituency_wikipedia_link)
constituency_geography = tables[1]
constituency_geo = constituency_geography.iloc[:, :5]
constituency_geo.columns = ["constituency","voting_pop",
							"sq_km", "voting_pop_density",
							"jurisdictions"]
constituency_geo.to_pickle("constituency_geo.pkl")
"""

constituency_geo = pd.read_pickle("constituency_geo.pkl")
constituency_geo = constituency_geo.iloc[:, :-1]
extended[-1] = pd.merge(cleaned_bios[-1], constituency_geo, how="left", on="constituency")
print(cleaned_bios[-1].shape)
print(extended[-1].shape)


to_remove_2 = ["sq_km", "voting_pop"]
extended[-1] = extended[-1].drop(columns=to_remove_2)
extended[-1]["lnpopudensity"] = np.log( extended[-1].voting_pop_density )
extended[-1] = extended[-1].drop(columns=["voting_pop_density"])



combined = pd.concat(extended) 


with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	print(combined)
combined.to_pickle("combined.pkl")






