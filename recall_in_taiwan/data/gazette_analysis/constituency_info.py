
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
	return output




# Import the beautifulsoup
# and request libraries of python.



leg_name_master = pd.read_pickle("leg_name_remastered.pkl")
investigate = pd.read_pickle("flag.pkl")




paper_data = pd.read_csv("paper_data.csv")



#	------*****----- Import cleaned_bios
cleaned_bio = "cleaned_bio_{}.pkl"
cleaned_bios = [ pd.read_pickle(cleaned_bio.format(2012 + i*4)  ) for i in range(3)]


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


indexed_paper_data = indexed_paper_data.merge(\
					pd.concat([cleaned_bios[i]for i in range(2)])\
					[ ["name_id", "term", "constit" ]  ],\
					how="left", left_on =["order", "name_id"],\
					right_on=["term", "name_id"])

indexed_paper_data.to_pickle("indexed_paper_data.pkl")





extended = [None] * 3
const_info = indexed_paper_data.loc\
				[ (indexed_paper_data.order == 8) &\
				(indexed_paper_data.dtier31 == 1),\
				["constit", "lnpopudensity"]]
const_info = const_info.drop_duplicates()
for i in range(  len(extended) -1 ):
	extended[i] = pd.merge\
				(cleaned_bios[i], const_info,\
				how="left", on="constit")
	extended[i] = extended[i].drop(columns=["constit"] ) 
# constituency info from paper data



# constituency info from outside

constituency_geo = pd.read_pickle("constituency_geo.pkl")
constituency_geo = constituency_geo.iloc[:, :-1]
extended[-1] = pd.merge(cleaned_bios[-1], constituency_geo, how="left", on="constituency")


to_remove_2 = ["sq_km", "voting_pop"]
extended[-1] = extended[-1].drop(columns=to_remove_2)
extended[-1]["lnpopudensity"] = np.log( extended[-1].voting_pop_density )
extended[-1] = extended[-1].drop(columns=["voting_pop_density"])



combined = pd.concat(extended) 


combined.to_pickle("combined.pkl")






