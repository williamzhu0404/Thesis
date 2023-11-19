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
"""
title = "^w*[\(（][0-9]+[\)）].+?(?=：)"
title_1 = "^\w*[(（][0-9]+[)）].+?(?=：)"
"""
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









"""
42               廖國棟Sufin‧Siluko        廖國棟        Sufin‧Siluko   
43               廖國棟Sufin．Siluko        廖國棟        Sufin．Siluko  
"""

"""

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

#leg_name_master.at[43, "name_regex"] = "(廖國棟|Sufin[．‧]Siluko)"


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





with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(leg_name_master )
"""
	



#leg_name_master.loc[chn_name_only, "name_regex" ] = leg_name_master.loc[chn_name_only, "name_chn"]









"""
leg_7_8_9_10["indigenous_name"] = leg_7_8_9_10["name"].str.extract()


leg_7_8_9_10_l = leg_7_8_9_10.values.tolist()
leg_7_8_9_10_l.sort()
for i in leg_7_8_9_10_l:
	print(i)
"""


legislator_infos = pd.read_csv("16_CSV_16_CSV.csv", parse_dates=[8, 13])

#	term             int64
#	name            object
#	ename           object
#	sex             object
#	party           object
#	partyGroup      object
#	areaName        object
#	committee       object
#	onboardDate     object
#	degree          object
#	experience      object
#	picUrl          object
#	leaveFlag       object
#	leaveDate       object
#	leaveReason     object


#	legislator_infos["onboardDate", "leaveDate"]

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

print(leg_name_master[leg_name_master.name == "谷辣斯．尤達卡Kolas Yotaka"].name_regex)


#	------*****------ Name change
leg_name_master.loc[leg_name_master.name == "游毓蘭", "name_regex"] = "[游葉]毓蘭"

#	She changed here name from 葉毓蘭 to 游毓蘭, zh.wikipedia.org says 1968年，游毓蘭的生父將她過繼給一位葉姓同事，因此改名為「葉毓蘭」
#	Okay, this is definitely the worst, the pdf is machine-readable EXCEPT when it comes to the name of 



leg_name_master.to_pickle("name_match.pkl")

"""
國108年11月29日（星期五）上午9時1分至9時5分、10時至11時6分
12月3日（星期二）上午9時至11時57分、下午2時30分至4時
13分、5時至5時1分
2019
Today is 2019-12-03 00:00:00

 
(1)「報告事項第二十四案委員柯建銘等所提復議案不予通過」部分：
出席人數：65 贊成人數：0 反對人數：65 棄權人數：0
贊成者：0 人
反對者：65 人
黃國書 鄭運鵬 周春米 吳玉琴 李俊俋
柯建銘 管碧玲 劉建國 尤美女 王定孙
鄭秀玲 黃國昌 徐永明 鍾孔炤 陳素月
吳琪銘 李麗芬 李鴻鈞 施義芳 許智傑
呂孫綾 吳思瑤 張宏陸 鍾佳濱 蕭美琴
羅致政 蔡培慧 蘇巧慧 趙天麟 陳靜敏
陳亭妃 黃秀芳 陳明文 蔡易餘 葉宜津
陳賴素美 余宛如 劉世芳 吳焜裕 余 天
邱泰源 邱志偉 何欣純 陳 瑩 蘇震清
蔡適應 陳歐珀 蔣絜安 洪宗熠 林靜儀
段宜康 何志偉 林岱樺 吳秉叡 邱議瑩
李昆澤 陳曼麗 王榮璋 郭正亮 賴瑞隆
蘇治芬 郭國文 莊瑞雄 林昶佐 洪慈庸
棄權者：0 人

國108年12月6日（星期五）上午9時至9時7分、10時至12時47分
12月10日（星期二）上午9時3分至12時16分、下午2時至4時59分
2019
Today is 2019-12-10 00:00:00

 
(1)「報告事項第二十六案國民黨黨團提議逕付二讀，由國民黨黨團負
責召集協商不予通過」部分：
出席人數：62 贊成人數：21 反對人數：41 棄權人數：0
贊成者：21 人
曾銘宗 陳宜民 林為洲 孔文卲 林麗蟬
呂玉玲 林奕華 賴士葆 許毓仁 簡東明
徐志榮 鄭天財 Sra Kacaw 柯呈枋 蔣乃辛
陳玉珍 柯志恩 王育敏 林德福 陳超明
黃昭順 顏寬恒
反對者：41 人
鄭寶清 鄭運鵬 周春米 吳玉琴 李俊俋
柯建銘 尤美女 王定孙 鍾孔炤 李麗芬
施義芳 呂孫綾 吳思瑤 張宏陸 鍾佳濱
蘇巧慧 陳靜敏 黃秀芳 陳明文 蔡易餘
葉宜津 江永昌 陳賴素美 余宛如 吳焜裕
余 天 邱泰源 邱志偉 何欣純 蔣絜孜
洪宗熠 林靜儀 段宜康 吳秉叡 李昆澤
陳曼麗 王榮璋 郭正亮 郭國文 莊瑞雄
洪慈庸
棄權者：0 人

(5)「討論事項第八案照民進黨黨團修正提議予以通過」部分：
出席人數：67 贊成人數：56 反對人數：11 棄權人數：0
贊成者：56 人
黃國書 鄭寶清 鄭運鵬 周春米 李俊俋
柯建銘 管碧玲 劉建國 尤美女 王定孙
鍾孔炤 陳素月 吳琪銘 李麗芬 施義芳
許智傑 呂孫綾 張廖萬堅 吳思瑤 張宏陸
林俊憲 鍾佳濱 蕭美琴 繫致政 蔡培慧
蘇巧慧 趙天麟 陳靜敏 陳亭妃 黃秀芳
林淑芬 江永昌 陳賴素美 劉世芳 余 天
邱泰源 邱志偉 何欣純 陳 瑩 蘇震清
蔡適應 陳歐珀 蔣絜孜 洪宗熠 段宜康
何志偉 林岱樺 吳秉叡 邱議瑩 李昆澤
王榮璋 郭正亮 賴瑞隆 蘇治芬 郭國文
莊瑞雄
反對者：11 人
曾銘宗 林麗蟬 林奕華 鄭秀玲 黃國昌
徐永明 李鴻鈞 周陳秀霞 許毓仁 王育敏
鄭天財 Sra Kacaw
棄權者：0 人

國106年11月3日（星期五）上午9時至9時28分、10時至11時54分、下午
2時47分至5時14分
11月7日（星期二）上午9時1分至10時34分、下午5時至5時16
分
2017

(2)「討論事項第一案產業創新條例第十二條之一照民進黨黨團修正動
議予以通過」」部分：
贊成者：62 人
黃國書 鄭寶清 呂孫綾 鍾佳濱 何欣純
柯建銘 劉櫂豪 劉建國 尤美女 鍾孔炤
陳素月 李麗芬 蔡適應 蔡易餘 施義芳
鄭運鵬 吳秉叡 吳琪銘 周春米 許智傑
林俊憲 邱議瑩 蕭美琴 羅致政 蔡培慧
蘇巧慧 陳其邁 黃秀芳 陳明文 葉宜津
吳玉琴 林淑芬 蘇震清 楊 曜 余宛如
劉世芳 吳焜裕 高志鵬 趙正孙 邱泰源
邱志偉 李俊俋 陳 瑩 管碧玲 陳賴素美
賴瑞隆 陳歐珀 洪宗熠 江永昌 段宜康
黃偉哲 林岱樺 吳思瑤 張宏陸 李昆澤
陳曼麗 王榮璋 郭正亮 張廖萬堅 蘇治芬
姚文智 莊瑞雄
反對者：25 人
林德福 李彥秀 曾銘宗 孔文卲 林麗蟬
呂玉玲 林昶佐 洪慈庸 黃國昌 徐永明
許淑華 羅明才 楊鎮浯 費鴻泰 賴士葆
許毓仁 鄭天財 蔣乃辛 蔣萬孜 馬文君
柯志恩 陳超明 黃昭順 顏寬恒 陳學聖
棄權者：0 人

國108年11月1日（星期五）上午9時至9時16分、10時1分至12時
11月5日（星期二）上午9時至9時26分、下午5時至5時4分
2019
Today is 2019-11-05 00:00:00

 
(1)「時付力量黨團提議變更議程第一案不予通過」部分：
出席人數：49 贊成人數：3 反對人數：44 棄權人數：2
贊成者：3 人
鄭秀玲 黃國昌 徐永明
反對者：44 人
黃國書 鄭寶清 鄭運鵬 周春米 吳玉琴
李俊俋 柯建銘 管碧玲 劉建國 尤美女
王定孙 鍾孔炤 吳琪銘 李麗芬 施罬芳
呂孫綾 張廖萬堅 鍾佳濱 羅致政 蔡培慧
陳靜敏 黃秀芳 蔡易餘 葉宜津 陳賴素美
余宛如 吳焜裕 余 天 邱泰源 邱志偉
蘇震清 蔡適應 蔣絜孜 林靜儀 段宜康
何志偉 吳秉叡 邱議瑩 李昆澤 陳曼麗
王榮璋 郭正亮 賴瑞隆 蘇治芬
棄權者：2 人
林奕華 林淑芬


17)「國民黨黨團針對議事日程草案提議增列討論事項第七案不予通過
」部分：
贊成者：26 人
林為洲 曾銘宗 孔文吉 林麗蟬 呂玉玲
張麗善 林德福 羅明才 楊鎮浯 費鴻泰
賴士葆 許毓仁 簡東明 徐志榮 鄭天財
陳宜民 李彥秀 蔣乃辛 盧秀燕 吳志揚
蔣萬安 馬文君 柯志恩 江啟臣 陳超明
王惠美
反對者：50 人
鄭寶清 劉櫂豪 蘇巧慧 鄭運鵬 李俊俋
柯建銘 葉宜津 劉建國 王定宇 鍾孔炤
陳素月 李麗芬 何欣純 莊瑞雄 施義芳
呂孫綾 吳秉叡 吳琪銘 周春米 許智傑
林俊憲 邱議瑩 蔡培慧 鍾佳濱 陳其邁
黃秀芳 陳明文 林靜儀 林淑芬 蘇震清
余宛如 江永昌 吳焜裕 邱泰源 蔡適應
陳 瑩 管碧玲 陳賴素美 陳歐珀 洪宗熠
Kolas otaka 劉世芳 段宜康 張宏陸
李昆澤 陳曼麗 王榮璋 郭正亮 蘇治芬
姚文智
棄權者：0 人

(21)「討論事項第一案外交及國防委員會第 78 案予以通過」部分：
出席人數：95 贊成人數：63 反對人數：32 棄權人數：0
贊成者：63 人
黃國書 鄭寶清 賴瑞隆 林靜儀 鄭運鵬
柯建銘 李俊俋 劉建國 尤美女 王定宇
林昶佐 高潞‧以用‧巴魕剌 Kawlo．Iyun．Pacidal
洪慈庸 黃國昌 徐永明 鍾孔炤 陳素月
李麗芬 周春米 劉櫂豪 施義芳 許智傑
呂孫綾 吳琪銘 吳思瑤 張宏陸 林俊憲
羅致政 蔡培慧 蘇巧慧 陳靜敏 黃秀芳
陳明文 蔡易餘 吳玉琴 林淑芬 蘇震清
楊 曜 余宛如 劉世芳 吳焜裕 邱泰源
邱志偉 何欣純 陳 瑩 管碧玲 陳賴素美
蔡適應 陳歐珀 洪宗熠 江永昌 陳超明
段宜康 林岱樺 吳秉叡 邱議瑩 李昆澤
陳曼麗 王榮璋 郭正亮 張廖萬堅 蘇治芬
莊瑞雄
反對者：32 人
江啟臣 曾銘宗 吳志揚 林為洲 孔文吉
林麗蟬 呂玉玲 林奕華 李鴻鈞 高金素梅
陳怡潔 周陳秀霞 許淑華 童惠珍 羅明才
費鴻泰 賴士葆 許毓仁 徐志榮 蔣乃辛
鄭天財 Sra Kacaw 李彥秀 蔣萬安 馬文君
柯志恩 王育敏 林德福 黃昭順 顏寬恒
陳學聖 廖國棟
棄權者：0 人

國110年1月20日（星期三）上午9時10分至10時23分
1月29日（星期五）上午11時30分至下午5時45分、5時59分至6
時35分
2021
Today is 2021-01-29 00:00:00

 
(1)「討論事項第一案通案部分第 19-1 案不予通過」部分：
出席人數：102 贊成人數：41 反對人數：58 棄權人數：3
贊成者：41 人
王婉諭 陳椒華 邱顯智 林為洲 林奕華
鄭麗文 江啟臣 李貴敏 吳怡玎 萬美玲
呂玉玲 蔡壁如 林思銘 陳雪生 葉毓蘭
楊瓊瓔 曾銘宗 張育美 孔文吉 賴士葆
吳斯懷 廖國棟 陳超明 費鴻泰 廖婉汝
魯明哲 李德維 鄭正鈐 洪孟楷 林文瑞
馬文君 許淑華 溫玉霞 徐志榮 林德福
謝衣鳯 鄭天財 Sra Kacaw 翁重鈞 羅明才
蔣萬安 陳以信
反對者：58 人
黃世杰 蘇巧慧 莊瑞雄 柯建銘 鄭運鵬
陳柏惟 陳歐珀 黃國書 李昆澤 郭國文
何志偉 何欣純 林宜瑾 管碧玲 趙天麟
鍾佳濱 劉櫂豪 張宏陸 洪申翰 余 天
劉建國 湯蕙禎 蔡適應 林岱樺 楊 曜
林楚茵 吳玉琴 賴品妤 黃秀芳 陳 瑩
江永昌 羅美玲 周春米 林淑芬 吳琪銘
范 雲 賴惠員 陳明文 陳亭妃 莊競程
劉世芳 張廖萬堅 伍麗華 Saidhai Tahovecahe
陳素月 蔡易餘 羅致政 王美惠 邱泰源
吳思瑤 高嘉瑜 邱議瑩 陳秀寳 沈發惠
吳秉叡 林俊憲 賴瑞隆 蘇治芬 邱志偉
棄權者：3 人
邱臣遠 張其祿 賴香伶

國109年12月24日（星期四）上午9時1分至11時52分、中午12時35分至
下午9時32分
2020
Today is 2020-12-24 00:00:00
Pause to check the date.

 
(1)「討論事項第一案學校衛生法第七條照民進黨黨團修正動議維持現
行條文不予修正予以通過」部分：
出席人數：107 贊成人數：59 反對人數：41 棄權人數：7
贊成者：59 人
黃世杰 蘇巧慧 莊瑞雄 柯建銘 鄭運鵬
陳柏惟 陳歐珀 黃國書 李昆澤 郭國文
何志偉 何欣純 林宜瑾 管碧玲 趙天麟
鍾佳濱 劉櫂豪 張宏陸 洪申翰 余 天
湯蕙禎 蔡適應 林岱樺 楊 曜 林楚茵
吳玉琴 許智傑 賴品妤 黃秀芳 陳 瑩
江永昌 羅美玲 周春米 王定宇 吳琪銘
范 雲 賴惠員 陳明文 陳亭妃 莊競程
劉世芳 張廖萬堅 伍麗華 Saidhai Tahovecahe
陳素月 蔡易餘 羅致政 王美惠 邱泰源
吳思瑤 高嘉瑜 邱議瑩 陳秀寳 沈發惠
吳秉叡 林俊憲 賴瑞隆 蘇治芬 邱志偉
林昶佐
反對者：41 人
王婉諭 陳椒華 邱顯智 林為洲 林奕華
鄭麗文 江啟臣 李貴敏 吳怡玎 萬美玲
呂玉玲 高金素梅 林思銘 陳雪生 葉毓蘭
楊瓊瓔 曾銘宗 張育美 陳玉珍 孔文卲
賴士葆 吳斯懷 陳超明 費鴻泰 廖婉汝
魯明哲 李德維 鄭正鈐 洪孟楷 林文瑞
馬文君 許淑華 溫玉霞 徐志榮 林德福
謝衣鳯 鄭天財 Sra Kacaw 翁重鈞 羅明才
蔣萬宊 陳以信
棄權者：7 人
蔡壁如 邱臣遠 高虹宊 張其祿 賴香伶
劉建國 林淑芬

國110年5月14日（星期五）上午9時至9時21分、10時4分至下午4時6分
5月18日（星期二）上午9時至10時31分
2021
(2)「討論事項第二案國家重點領域產學合作及人才培育創新條例第三
條照民進黨黨團修正動議條文予以通過」部分：
出席人數：95 贊成人數：54 反對人數：35 棄權人數：6
贊成者：54 人
范 雲 莊競程 羅致政 柯建銘 劉世芳
陳歐珀 黃國書 李昆澤 黃世杰 林俊憲
何欣純 林宜瑾 管碧玲 鍾佳濱 劉櫂豪
張宏陸 余 天 劉建國 湯蕙禎 蔡適應
林岱樺 楊 曜 林楚茵 吳玉琴 許智傑
賴品妤 陳 瑩 江永昌 羅美玲 周春米
王定孙 吳琪銘 郭國文 賴惠員 陳亭妃
何志偉 鄭運鵬 張廖萬堅 陳素月 莊瑞雄
伍麗華 Saidhai Tahovecahe 趙正孙 王美惠
邱泰源 吳思瑤 高嘉瑜 邱議瑩 陳秀寳
沈發惠 吳秉叡 蘇巧慧 賴瑞隆 蘇治芬
邱志偉
反對者：35 人
王婉諭 陳椒華 邱顯智 費鴻泰 鄭麗文
陳玉珍 江啟臣 李貴敏 吳怡玎 萬美玲
呂玉玲 林思銘 陳雪生 葉毓蘭 楊瓊瓔
曾銘宗 張育美 賴士葆 吳斯懷 陳超明
林為洲 廖婉汝 魯明哲 李德維 鄭正鈐
洪孟楷 林文瑞 馬文君 林奕華 許淑華
溫玉霞 徐志榮 林德福 謝衣鳯 陳以信
棄權者：6 人
蔡壁如 邱臣遠 高虹孜 張其祿 賴香伶
洪申翰

國109年4月17日（星期五）上午9時至9時38分、10時1分至12時34分
4月21日（星期二）上午10時31分至下午2時13分
2020
Today is 2020-04-21 00:00:00

(5)「討論事項第一案嚴重特殊傳染性肺炎防治及紓困振興特別條例委
員曾銘宗等提案增訂第九條之四不予通過」部分：
出席人數：99 贊成人數：39 反對人數：60 棄權人數：0
贊成者：39 人
林為洲 蔣萬孜 林奕華 江啟臣 李貴敏
吳怡玎 萬美玲 呂玉玲 傅 萁 林思銘
陳雪生 葉毓蘭 楊瓊瓔 曾銘宗 張育美
陳玉珍 孔文卲 賴士葆 吳斯懷 廖國棟
陳超明 費鴻泰 廖婉汝 魯明哲 李德維
鄭正鈐 洪孟楷 林文瑞 馬文君 許淑華
溫玉霞 徐志榮 林德福 翁重鈞
鄭天財 Sra Kacaw 羅明才 鄭麗文 陳以信
反對者：60 人
黃秀芳 邱泰源 鍾佳濱 柯建銘 鄭運鵬
陳柏惟 陳歐珀 黃國書 李昆澤 郭國文
何志偉 何欣純 管碧玲 趙天麟 王美惠
劉櫂豪 張宏陸 洪申翰 余 天 劉建國
湯蕙禎 蔡適應 林岱樺 楊 曜 林楚茵
吳玉琴 許智傑 賴品妤 黃世杰 陳 瑩
江永昌 蘇震清 羅美玲 吳秉叡 王定孙
林淑芬 吳琪銘 范 雲 賴惠員 陳明文
莊競程 劉世芳 張廖萬堅 陳素月 蔡易餘
伍麗華 Saidhai Tahovecahe 羅致政 趙正孙
莊瑞雄 蘇巧慧 吳思瑤 高嘉瑜 邱議瑩
沈發惠 周春米 林俊憲 賴瑞隆
蘇治芬 林昶佐
棄權者：0 人


國109年4月17日（星期五）上午9時至9時38分、10時1分至12時34分
4月21日（星期二）上午10時31分至下午2時13分
2020
Today is 2020-04-21 00:00:00
My own counts: 8 52 2
Recorded counts:  [8, 52, 2]
My own counts: 39 64 0
Recorded counts:  [39, 64, 0]
My own counts: 38 61 5
Recorded counts:  [38, 61, 5]
My own counts: 36 59 5
Recorded counts:  [38, 60, 5]
My own counts: 37 59 0
Recorded counts:  [39, 60, 0]
My own counts: 0 56 3
Recorded counts:  [0, 56, 3]
My own counts: 0 58 0
Recorded counts:  [0, 58, 0]
"""
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
			#print("matched pattern:", pat_series[i])
			#print("matched index:", i)
			return i
	return None





def assign_ind_series(pat_series, name_series, val, output):
	count_zero = True
	for name in name_series:
		#print("name to be matched:",name)
		match = assign_ind(pat_series, name)
		if match is not None:
			#print("match is successful!")
			#count += 1
			output.iat[match] = val
			if count_zero:
				count_zero = False
		#else:
			#input("Pause")
			#print("Wait?")
	if count_zero:
		#print(output.value_counts() )
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
	print(txt)
	match = re.search( ROC_TIME_LOC, txt, re.DOTALL)
	if match is None:
		raise Exception("Time information not located")
	time_txt = match.group().replace(' ', '')
	print(time_txt)
	years = re.findall(ROC_YEAR, time_txt)
	if len(years) == 1:
		roc_year = re.search( ROC_YEAR_NUM, years[0]).group()
		gregorian_year = int(roc_year) + ROC_YEAR_ZERO
		print(gregorian_year)
		date_txts = re.findall(CHN_MMDD_FORMAT, time_txt)	
		date_txts = ["{}年".format(gregorian_year) + date for date in date_txts]
		dates = [datetime.strptime(chn_date, '%Y年%m月%d日') for chn_date in date_txts]
		print("Today is {}".format(dates[-1]))
		return dates
		#return [date.replace(year=gregorian_year) for date in dates]
	else:
		date_txts = re.findall(ROC_DATE_FORMAT, time_txt)	
		year_num_inds = [   (   ind, re.search(ROC_YEAR_NUM, date).group()  )
							for ind, date in enumerate(date_txts)
								if re.search(ROC_YEAR_NUM, date) is not None ]
		year_num_inds = [(ind, int(year) + ROC_YEAR_ZERO ) for ind, year in year_num_inds]
		date_txts = re.findall(CHN_MMDD_FORMAT, time_txt)	
		print(year_num_inds)
		end_inds = [element[0] for element in year_num_inds  ][1:]
		end_inds.append(len(date_txts) )
		print(end_inds)
		for i in range(  len(year_num_inds)  ):
			for j in range(year_num_inds[i][0], end_inds[i]):
				print(j)
				date_txts[j] = "{}年".format(year_num_inds[i][1]) + date_txts[j]
		dates = [datetime.strptime(chn_date, '%Y年%m月%d日') for chn_date in date_txts]
		print("Today is {}".format(dates[-1]))
		print(years)
		print(year_num_inds)
		return dates
		#raise Exception("Someone's trying to work on New Year's Eve?")
#	Extracting hour is too much work
#	You get dates only


def extract_leg_presents_lines(pdf):
	txt = extract_info_lines(pdf)
	print(txt)
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
	print('\n', txt)
	rec_txts = re.findall(REC_DELIMITERS, txt, flags=re.DOTALL)
	if troubleshoot:
		for ind, rec_txt in enumerate(rec_txts):
			rec_nums = re.findall(title_num, rec_txt)
			#if ind == 3:
				#print(rec_txt)
				#print(ind, rec_nums[0])
				#input("Pause for reflection")
			if len(rec_nums) == 1:
				if ind + 1 != int(rec_nums[0]):
					print(rec_txt)
					print(ind, rec_nums[0])
					raise Exception("The matched rcv has the wrong index!") 
			elif len(rec_nums) == 0:
				print(ind)
				raise Exception("Somehow the index of the rcv is not included!")
			else:
				print(ind)
				raise Exception("Somehow multiple rcvs are included!")
	return rec_txts

def divide_camp(rec_txt):
	print("DIVISION, CLEAR THE LOBBY!")
	print(rec_txt)
	rec_name = re.search(title, rec_txt, re.DOTALL).group()
	rec_votes = re.search(  "{}.+".format(camp) , rec_txt , re.DOTALL  ).group()
	#print(rec_name)
	#print(rec_votes)	
	votes = tags(rec_votes)
	#print(votes)
	start_inds = [ind for ind in range(len(votes)) if re.search(camp, votes[ind]) is not None ]
	ind_count = len(start_inds)
	if ind_count > 3:
		print(votes)
		raise Exception("Way too many camps for some reason") 
	elif ind_count < 3:
		print(votes)
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
	#for i in start_inds:
	#	print(re.search(title_num, recs[i]).group()  )
	rec_nums = len(start_inds)
	end_inds = start_inds[1:]
	end_inds.append(len(recs) )
	#for start in start_inds:
		#print( recs[start] )
	return [recs[start_inds[i]: end_inds[i] ]for i in range(rec_nums)  ]


def assign_rcv_votes(rec, output, pat_series):
	# we have (name, [[yea,...], [nay,...], [abstain,...]])
	name = rec[0]
	flag = 0
	camp_names = rec[1]
	strengths = [int( re.search(camp_strength, camp_names[i][0]).group() ) for i in range( len(rec[1]) ) ]
	yea_count = assign_ind_series(pat_series, camp_names[0][1:], 1, output)
	nay_count = assign_ind_series(pat_series, camp_names[1][1:], 2, output)
	abstain_count = assign_ind_series(pat_series, camp_names[2][1:], 3, output)
	print("My own counts:", yea_count, nay_count, abstain_count)
	print("Recorded counts: ", strengths)
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
	print(sign_post)
	yea = rec[ sign_post[0]+1 : sign_post[1]  ]
	nay = rec[ sign_post[1]+1 : sign_post[2]  ]
	abstain = rec[ sign_post[2]+1 :  ]
	yea_count = assign_ind_series(pat_series, yea, 1, output)
	nay_count = assign_ind_series(pat_series, nay, 2, output)
	abstain_count = assign_ind_series(pat_series, abstain, 3, output)
	#print("My own counts:", yea_count, nay_count, abstain_count)
	#print("The recorded countes: ", strengths)
	if yea_count != strengths[0]:
		raise Exception("The recorded yea number differ from the minute record")
	elif nay_count != strengths[1]:
		raise Exception("The recorded nay number differ from the minute record")
	elif abstain_count != strengths[2]:
		raise Exception("The recorded abstention number differ from the minute record")
	else:
		return [name, output]



#def assign_serving(pdf):
def assign_serving(pdf, output, info_df, pat_series):
	first_page = pdf.pages[0].extract_text()
	#print(first_page.split('\n')[0])
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
	#print( pd.concat([pat_series, output], axis=1) )


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
		


"""
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
	print(test)


trouble = "/Users/williamzhu/Downloads/minute_105_2016/LCEWC03_09010101.pdf"
trouble_pdf = pdfplumber.open(trouble)
trouble_page = trouble_pdf.pages[216].extract_text()
trouble_page_1 = trouble_pdf.pages[209].extract_text()
print(trouble_page)
print(trouble_page_1)

trouble = extract_rcv_txt(trouble_pdf)
print(trouble)
trouble_shoot = extract_rcv_recs(trouble_pdf, troubleshoot=False, troubleshoot_1=True)
input("Pause")
"""



# import required module

# assign directory
directories = ["/Users/williamzhu/Downloads/ly_minute_08",
			"/Users/williamzhu/Downloads/ly_minute_09",
		 	"/Users/williamzhu/Downloads/ly_minute_10"]
	



# iterate over files in
# that directory
"""
rcv_records = [None, None, None]
irregular = [None, None, None]
for ind, directory in enumerate(directories):	
	files = Path(directory).glob('*.pdf')
	initialized = False
	for file in files:
		with pdfplumber.open(file) as pdf:
			if find_rcv_page(pdf):
				print("Examining:", file)
				if not initialized:
					rcv_records[ind] = add_rcv_rows(pdf)	
					initialized = True
				else:
					rcv_records[ind] = add_rcv_rows(  pdf, rec_df=rcv_records[ind]  )
	rcv_records[ind].to_pickle( "./rcv_{:02d}.pkl".format(ind + 8)  )  
	irregular[ind] = rcv_records[ind][rcv_records[ind].flag != 0]
	irregular[ind].to_pickle( "./irregular_rcv_{:02d}.pkl".format(ind + 8)  )  
	with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
		print(irregular[ind])
"""
rcv_records = [pd.read_pickle(  "./rcv_{:02d}.pkl".format(ind + 8)  ) for ind in range(3)    ] 
irregular = [pd.read_pickle(  "./irregular_rcv_{:02d}.pkl".format(ind + 8)  )  for ind in range(3)    ] 

 







#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090207.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_09080101.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090812.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090813.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090109.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090808.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_090312.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_09060101.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/02LCEWC03_10020102.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/14LCEWC03_100614.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/12LCEWC03_100312.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/14LCEWC03_100414.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100109.pdf"
#trouble_file = "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100101.pdf"

"""
trouble_file_0 = "/Users/williamzhu/Downloads/ly_minute_09/LCEWC03_09060101.pdf"
trouble_file_1 = "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100101.pdf"
trouble_file_2 = "/Users/williamzhu/Downloads/ly_minute_10/LCEWC03_100109.pdf"

trouble_files = [trouble_file_0, trouble_file_1, trouble_file_2]
for trouble_file in trouble_files:
	trouble_pdf = pdfplumber.open(trouble_file)
	trouble_rcv = add_rcv_rows(trouble_pdf)
"""


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


"""
rcv_records[-1].loc[meeting_indices, fu_vote] = fu
rcv_records[-1].loc[meeting_indices, chen_vote] = chen
"""




chen_1 = 2 
"""
rcv_records[-1].loc[(title_1)|(title_2), chen_vote] = chen_1
"""

"""
rcv_records[-1].to_pickle(  "./rcv_10_updated.pkl")
"""






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

