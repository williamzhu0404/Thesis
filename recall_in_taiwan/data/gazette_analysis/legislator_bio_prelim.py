
# Import the beautifulsoup
# and request libraries of python.

from pathlib import Path


import re

import numpy as np
import pandas as pd


NO_PARTY = 999
ROC_YEAR_ZERO = 1911


leg_name_master = pd.read_pickle("name_match.pkl")
investigate = pd.read_pickle("flag.pkl")
Legislator_Infos = pd.read_csv("16_CSV_16_CSV.csv")


leg_7_10 = Legislator_Infos[Legislator_Infos.term > 6]





#	CUSTOM-DESIGNED, MODIFY WITH CARE
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


def read_elected_info(file, colnames, elected=True, remove="'"):
	df = pd.read_csv(file, header=None, names=colnames, index_col=False)
	if len(remove) > 0:
		df = df.replace({remove:''}, regex=True)
	print(df.dtypes)
	#input("Pause to see the datatpes.")
	raw_row = df.shape[0]
	convert_to_pd_int(df)			
	converted_row = df.shape[0]
	if converted_row != raw_row:
		print("HELP, something is WRONG!")
		raise Exception("Conversion is problematic.")
	return df[df.elected == "*"] if elected else df


def replace_with_dict(df, col_name, col_dict):
	df = df.replace({col_name: col_dict})
	df[ [col_name] ] = df[ [col_name] ].astype(  dtype=pd.Int64Dtype()  )
	return df


leg_name_master = pd.read_pickle("name_match.pkl")
investigate = pd.read_pickle("flag.pkl")
Legislator_Infos = pd.read_csv("16_CSV_16_CSV.csv", parse_dates=[8, 13])

convert_to_pd_int(Legislator_Infos)








leg_name_master["name_id"] = leg_name_master.index.astype(  dtype=pd.Int64Dtype()  )


leg_name_master.to_pickle("leg_name_remastered.pkl")



Legislator_Infos = Legislator_Infos.dropna(how="all", axis="columns")
#	Remove photos
Legislator_Infos = Legislator_Infos.drop(columns=["picUrl"])
#	Remove experience 
Legislator_Infos = Legislator_Infos.drop(columns=["experience"])
#	Remove committee
Legislator_Infos = Legislator_Infos.drop(columns=["committee"])
#	Remove degree
Legislator_Infos = Legislator_Infos.drop(columns=["degree"])




#	------*****------	Change the string to Int64!!!!!
sex_dict = {"男": 1, "女": 2}
Legislator_Infos = replace_with_dict(Legislator_Infos, "sex", sex_dict)






leg_7_10 = Legislator_Infos[Legislator_Infos.term > 6]





leg_7_10 = merge_regex(leg_name_master.iloc[:, -2:], leg_7_10)
indexed_leg_infos = merge_regex(leg_name_master.iloc[:, -2:], Legislator_Infos)
indexed_leg_infos.to_pickle("indexed_leg_info.pkl")





colnames = ["prov_metro", "county", "district", "subcounty", "village",
			"ballot_num", "name", "party_id", "sex",
			"birth_date", "age", "place_of_birth",
			"degree", "incumbent", "elected"]


colnames_pr = [ "party_id", "ballot_num", "name", "sex",
			"birth_date", "age", "place_of_birth",
			"degree", "incumbent", "elected"]
	






path_root = "/Users/williamzhu/Thesis/recall_in_taiwan/data/electoral_data/votedata/voteData/"

first_level = ["/Users/williamzhu/Thesis/recall_in_taiwan/data/electoral_data/votedata/voteData/20120114-總統及立委_1",
				"/Users/williamzhu/Thesis/recall_in_taiwan/data/electoral_data/votedata/voteData/2016總統立委",
				 "/Users/williamzhu/Thesis/recall_in_taiwan/data/electoral_data/votedata/voteData/2020總統立委"]
second_level = ["區域立委", "平地立委", "山地立委", "不分區政黨"]
non_pr_level = second_level[:3]

file_pat = ["elbase", "elcand", "elctks", "elpaty", "elprof"]


leg_08 = leg_7_10[leg_7_10.term == 8]
leg_09 = leg_7_10[leg_7_10.term == 9]
leg_10 = leg_7_10[leg_7_10.term == 10]




leg_records = [leg_08, leg_09, leg_10]


commission_record =[  [None]*4, [None]*4, [None]*4]






				
for ind_1, level_1 in enumerate(first_level):
	pr_path = Path(  level_1, second_level[-1]  )
	pr_files = Path(pr_path).glob('elrepm*')
	party_files = Path(pr_path).glob('elpaty*')
	for file in party_files:
		df = read_elected_info(file,["party_num", "party"], False)
		leg_records[ind_1] = leg_records[ind_1].merge(df, how="left", on="party")
		leg_records[ind_1][ ["party_num"] ] = leg_records[ind_1][ ["party_num"] ].fillna(NO_PARTY)
		df[  ["party_group_num"]  ] = df[ ["party_num"]  ]
		leg_records[ind_1] = leg_records[ind_1].merge(df[  ["party", "party_group_num"]  ] ,
													how="left",
													left_on="partyGroup",
													right_on="party")
		leg_records[ind_1][ ["party_group_num"] ] = leg_records[ind_1][ ["party_group_num"] ].fillna(NO_PARTY)
	for file in pr_files:
		df = read_elected_info(file, colnames_pr, False, "'")
		commission_record[ind_1][-1] = merge_regex(leg_name_master.iloc[:, -2:], df)
	for ind_2, level_2 in enumerate(non_pr_level):
		non_pr_path = Path(level_1, level_2)
		files = Path(non_pr_path).glob('elcand*')
		for file in files:
			df = read_elected_info(file, colnames, True, "'")
			commission_record[ind_1][ind_2] = merge_regex(leg_name_master.iloc[:, -2:], df)


degree_dict = {"博士": 6,
				"碩士": 5,
				"大學": 4,
				"大專": 3,
				"專科": 3,
				"高中": 2,
				"高中(職)": 2,
				"其他": 1,
				}

incumbent_dict = {"Y": 1,
			"N": 2}



#	Let's change the values of electoral returns here
for ind, infos in enumerate(commission_record):
	election = pd.concat(infos)
	election = election.drop(columns=["subcounty", "village"])
	election = replace_with_dict(election, "degree", degree_dict)
	election = replace_with_dict(election, "incumbent", incumbent_dict)
	if ind == 0:
		election.birth_date = election.birth_date.astype(  dtype=pd.Int64Dtype()  )
	election.birth_date = election.birth_date + ROC_YEAR_ZERO * 10000
	election.birth_date = pd.to_datetime(election.birth_date, format='%Y%m%d')
	leg_info = pd.merge(leg_records[ind], election, on="name_id", how="left")
	pr_cols = commission_record[ind][-1].columns
	leg_records[ind] = leg_info









prof_cols = [0, 1, 2, 6, 7, 8, 9, 10, 17, 18, 19]
prof_colnames = ["prov_metro", "county", "district", 
			"valid_votes", "invalid_votes", "total_votes", "electorate", "pop",
			"electorate_over_pop_pct", "total_votes_over_electorate_pct", "elected_over_cands_pct"]

ctks_colnames = ["prov_metro", "county", "district", "subcounty", "village",
			"polling_station", "ballot_num",
			"vote", "vote_over_total_votes_pct", "elected"]
ctks_summary_colnames = ["prov_metro", "county", "district", "ballot_num",
						"vote", "vote_over_total_votes_pct", "elected"]

				
district_id_cols = ["prov_metro", "county", "district"]


prof_dfs = [None] * 3
ctks_dfs = [None] * 3


for ind_1, level_1 in enumerate(first_level):
	pr_path = Path(  level_1, second_level[0]  )
	pr_files = Path(pr_path).glob('elprof*')
	for file in pr_files:
		df = read_elected_info(file, None, False, "'")
		with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
			district_level = df[  (df.iloc[:,3] == 0) & (df.iloc[:, 2] != 0) ] 
			district_level = district_level[prof_cols]
			district_level.columns = prof_colnames
			prof_dfs[ind_1] = district_level


for ind_1, level_1 in enumerate(first_level):
	pr_path = Path(  level_1, second_level[0]  )
	pr_files = Path(pr_path).glob('elctks*')
	for file in pr_files:
		elu_cands = read_elected_info(file, ctks_colnames, True, "'")#, False)
		all_cands = read_elected_info(file, ctks_colnames, False, "'")
		with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
			elu_district_level = elu_cands[  (elu_cands.iloc[:,3] == 0) & (elu_cands.iloc[:, 2] != 0) ] 
			district_summary = elu_district_level[ctks_summary_colnames]
			all_elu_district_level = all_cands[  (all_cands.iloc[:,3] == 0) & (all_cands.iloc[:, 2] != 0) ] 
			condensed_vote = district_id_cols + ["vote"]
			condensed_vote_pct = district_id_cols + ["vote_over_total_votes_pct"]
			condensed_elus = all_elu_district_level[ condensed_vote ]
			condensed_elus_pct = all_elu_district_level[ condensed_vote_pct ]
			for colnames in [condensed_vote, condensed_vote_pct]:
				runner_up = all_elu_district_level[ colnames ].sort_values(colnames[-1], ascending=False).groupby(district_id_cols, sort=False, as_index=False).nth(1)
				winner = all_elu_district_level[ colnames ].sort_values(colnames[-1], ascending=False).groupby(district_id_cols, sort=False, as_index=False).nth(0)
				combined = pd.merge(runner_up, winner, how="inner", on=district_id_cols)
				margin = combined[  "{}_y".format(colnames[-1])  ] - combined[  "{}_x".format(colnames[-1])  ]
				new_col = "{}_margin".format( colnames[-1] )
				combined[new_col ] = margin
				margin_id = combined[ district_id_cols + [new_col]  ]
				district_summary = pd.merge(  district_summary, margin_id, how="inner", on=district_id_cols  )
			ctks_dfs[ind_1] = district_summary






combined_electoral_return = [ pd.merge(prof_dfs[i], ctks_dfs[i], how="inner", on=district_id_cols  )    for i in range(3)  ]
combined_electoral_return = [ pd.merge(  leg_records[i], combined_electoral_return[i], how="left", on=district_id_cols  ) for i in range(3) ]
with pd.option_context('display.max_rows', None, 'display.max_columns', None):#   more options can be specified also
	for i in range(3):
		combined_electoral_return[i].to_pickle("combined_electoral_return_{}.pkl".format(2012 + i*4))






