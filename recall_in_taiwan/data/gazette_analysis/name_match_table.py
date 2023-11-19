import re


import numpy as np
import pandas as pd


# Regex pattern variables and match functions

RCV_BEGIN = "本次會議各項記名表決結果名單："


CHN_CHAR = "[\u4E00-\u9FFF]"
CHN_CHAR_1 = "[一-鿆]"
ENG_LOWER = "[a-z]"
ENG = "[a-zA-Z]"

name_match   = "{}+".format(CHN_CHAR_1)
name_match_1 = "{0}+.*?{1}".format(CHN_CHAR_1, ENG_LOWER)

chn_name = "{0}.+?(?= |\n)".format(CHN_CHAR_1)




chn_name_ind_ext_template = "({1}{0}.+?(?= {0}|\n|$| [A-Z][a-z]* [A-Z][a-z]*)|[A-Z][a-z]* [A-Z][a-z]*)"
leg_name = chn_name_ind_ext_template.format(CHN_CHAR_1, "")
title = "\([0-9]+\).+?(?=：)"
title_num = "\([0-9]+\)"
camp = "[贊反棄].者：[0-9]+"
combined = "{0}|{1}|".format(title, camp)

ext_search = chn_name_ind_ext_template.format(CHN_CHAR_1, combined)


# Table wrangling

Legislator_Infos = pd.read_csv("16_CSV_16_CSV.csv")

leg_7_8_9_10 = Legislator_Infos[Legislator_Infos.term > 6]["name"].drop_duplicates().sort_values()
leg_7_8_9_10.str.strip()
leg_7_8_9_10.reset_index(drop=True, inplace=True)


leg_name_master = pd.concat(
					[leg_7_8_9_10,
					leg_7_8_9_10.str.extract(  "(^[^a-zA-Z ]*)"  ),
					leg_7_8_9_10.str.extract(  "({}.*)".format(ENG)),
					leg_7_8_9_10.str.extract(  "({}.*)".format(ENG))],
					axis=1
					)


leg_name_master.columns = ["name", "name_chn", "name_indig","name_regex"]



chn_name_rep = leg_name_master.duplicated(subset = "name_chn", keep = "last")
rep_inds = leg_name_master[chn_name_rep].index


leg_name_master.drop(rep_inds, inplace=True)

chn_name_only = leg_name_master["name_indig"].isnull()
leg_name_master.loc[chn_name_only, "name_regex" ] = leg_name_master.loc[chn_name_only, "name_chn"]


# Handling indgienous names
leg_name_master["name_regex"] = np.where(  leg_name_master["name_indig"].notnull()  ,
										"("+ leg_name_master["name_chn"].astype(str) +"|"+ leg_name_master["name_indig"]+")",
										leg_name_master["name_regex"])
# Handling delimiters between indigenous names
leg_name_master["name_regex"] = leg_name_master["name_regex"].str.replace(r"[ ．‧]", "[ ．‧]", regex=True)
# Indigenous names for which Chinese transliteration of some of their parts contains only two Chinese characters
leg_name_master["name_regex"] = leg_name_master["name_regex"].str.replace("(?<=[^一-鿆][一-鿆])(?=[一-鿆][^一-鿆])"," *", regex=True)
# Two-character Chinese names
leg_name_master["name_regex"] = leg_name_master["name_regex"].str.replace("(?<=^[一-鿆])(?=[一-鿆]$)"," *", regex=True)


leg_name_master.reset_index(drop=True, inplace=True)






leg_name_master.to_pickle("name_match.pkl")


