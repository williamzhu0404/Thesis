library(reticulate)
library(this.path)


library(haven)

setwd(here())






source_python("get_pickle.py")
pickle_data <- read_pickle_file("./rcv_09.pkl")

Rollcall_vote_merge_5_8_V_10 <- read_dta("Thesis/recall_in_taiwan/data/liao_2022_data/Rollcall vote merge_5-8_V.10.dta")

colnames(Rollcall_vote_merge_5_8_V_10)

# [1] "order"yes          "name"yes           "mpid"better           "party"maybe          "edu"yes            "gender"yes         "category"yes       "bir_year"yes      
# [9] "term"yes           "vote_get"yes       "vote_rate"yes      "con_size"yes       "lre"(maybe)            "lgo"(maybe)            "lchief"(maybe)         "pfa"(no)           
# [17] "cre"(no)            "govmember"(yes!)      "partyswitch"(hard, maybe necessary)    "leave"(yes)          "newcomer"(yes)       "faction"(maybe)        "personid" (yes)      "chair"(yes)         
# [25] "termsquare"     "termlog"        "termlog10"      "tier3"          "dtier31"        "dtier32"        "dtier33"        "tier2"         (yes)
# [33] "dtier21"        "dtier22"        "reform"         "csm"            "party4"         "csm2"           "edu3"           "deviall"       (yes)
# [41] "abstain"        "against"        "caseid"         "age"            "chairtime"      "deviall2"       "abstain2"       "against2"      
# [49] "lnpopudensity"  "pupdensity_new" "lcpolitics"     "lcpolitics2"    "absence"        "tier2n"         "dtier2n1"       "dtier2n2"      
# [57] "sntv"           "sntvlowdm"      "sntvhighdm"     "aboriginal"     "pluralitysmd"   "prlinked"       "prindep"        "elecsecurity"  
# [65] "lndm" 



