library(dplyr)
library(tidyr)
library(readr)

bill_proposal <- read_csv("Thesis/recall_in_taiwan/data/bill_proposal.csv", 
                          col_types = cols(date = col_integer(), 
                                           term = col_integer(), sessionPeriod = col_integer(), 
                                           sessionTimes = col_integer()))

ROC_0 = 1911

cleaned_df <- bill_proposal %>% mutate(ce_date =  
                                         as.Date(
                                           as.character(
                                             as.integer(date +ROC_0 * 10000)
                                           ), format = "%Y%m%d"
                                         ), .before = date)
saveRDS(cleaned_df, file = "bill_proposal")
View(cleaned_df)
