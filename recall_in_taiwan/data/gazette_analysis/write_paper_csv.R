library(haven)
library(readr)
library(dplyr)
library(tidyr)


Rollcall_vote_merge_5_8_V_10 <- read_dta("~/Thesis/recall_in_taiwan/data/liao_2022_data/Rollcall vote merge_5-8_V.10.dta")


View(Rollcall_vote_merge_5_8_V_10)



Rollcall_vote_merge_5_8_V_10 %>% colnames()

group_1 <- c(3: 25)
group_2 <- c(28: 39)
group_3 <- c(43: 45)
group_4 <- c(51: 52)
group_5 <- c(54: 63)
integer_cols <- c(1,
                  group_1,
                  group_2,
                  group_3,
                  group_4,
                  group_5)
Rollcall_vote_merge_5_8_V_10 <- Rollcall_vote_merge_5_8_V_10 %>% 
  mutate_at(integer_cols, as.integer)

View(Rollcall_vote_merge_5_8_V_10)





write_csv(Rollcall_vote_merge_5_8_V_10, "paper_data.csv")
