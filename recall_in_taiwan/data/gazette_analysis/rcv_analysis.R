library(readr)
library(haven)


library(fixest)
library(modelsummary)


library(dplyr)
library(ggplot2)

library(patchwork)

library(this.path)

cbp1 <- c("#999999", "#E69F00", "#56B4E9", "#009E73",
          "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

setwd(here())

Rollcall_vote_merge_5_8_V_10 <- read_dta("~/Thesis/recall_in_taiwan/data/liao_2022_data/Rollcall vote merge_5-8_V.10.dta")




defection_1 <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_term_type_1.csv", 
                 col_types = cols(...1 = col_integer(), 
                                  name_id = col_integer(), #session = col_integer(), 
                                  term = col_integer(), sex = col_integer(), 
                                  onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                  leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                  party_num = col_integer(), party_group_num = col_integer(), 
                                  birth_date = col_datetime(format = "%Y-%m-%d"), 
                                  age = col_integer(), degree = col_integer(), 
                                  incumbent = col_integer(), valid_votes = col_integer(), 
                                  total_votes = col_integer(), electorate = col_integer(), 
                                  pop = col_integer(), vote = col_integer(), 
                                  vote_margin = col_integer(), tier = col_integer(), 
                                  experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                  defect_period = col_integer(), president = col_integer(), 
                                  vice_president = col_integer()))
View(test)
defection_2  <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_term_type_2.csv", 
                 col_types = cols(...1 = col_integer(), 
                                  name_id = col_integer(), #session = col_integer(), 
                                  term = col_integer(), sex = col_integer(), 
                                  onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                  leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                  party_num = col_integer(), party_group_num = col_integer(), 
                                  birth_date = col_datetime(format = "%Y-%m-%d"), 
                                  age = col_integer(), degree = col_integer(), 
                                  incumbent = col_integer(), valid_votes = col_integer(), 
                                  total_votes = col_integer(), electorate = col_integer(), 
                                  pop = col_integer(), vote = col_integer(), 
                                  vote_margin = col_integer(), tier = col_integer(), 
                                  experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                  defect_period = col_integer(), president = col_integer(), 
                                  vice_president = col_integer()))
defection_3  <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_term_type_3.csv", 
                         col_types = cols(...1 = col_integer(), 
                                          name_id = col_integer(), #session = col_integer(), 
                                          term = col_integer(), sex = col_integer(), 
                                          onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                          leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                          party_num = col_integer(), party_group_num = col_integer(), 
                                          birth_date = col_datetime(format = "%Y-%m-%d"), 
                                          age = col_integer(), degree = col_integer(), 
                                          incumbent = col_integer(), valid_votes = col_integer(), 
                                          total_votes = col_integer(), electorate = col_integer(), 
                                          pop = col_integer(), vote = col_integer(), 
                                          vote_margin = col_integer(), tier = col_integer(), 
                                          experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                          defect_period = col_integer(), president = col_integer(), 
                                          vice_president = col_integer()))

defection_1_ext <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_session_type_1.csv", 
                        col_types = cols(...1 = col_integer(), 
                                         name_id = col_integer(), session = col_integer(), 
                                         term = col_integer(), sex = col_integer(), 
                                         onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                         leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                         party_num = col_integer(), party_group_num = col_integer(), 
                                         birth_date = col_datetime(format = "%Y-%m-%d"), 
                                         age = col_integer(), degree = col_integer(), 
                                         incumbent = col_integer(), valid_votes = col_integer(), 
                                         total_votes = col_integer(), electorate = col_integer(), 
                                         pop = col_integer(), vote = col_integer(), 
                                         vote_margin = col_integer(), tier = col_integer(), 
                                         experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                         defect_period = col_integer(), president = col_integer(), 
                                         vice_president = col_integer()))
defection_2_ext <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_session_type_2.csv", 
                            col_types = cols(...1 = col_integer(), 
                                             name_id = col_integer(), session = col_integer(), 
                                             term = col_integer(), sex = col_integer(), 
                                             onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                             leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                             party_num = col_integer(), party_group_num = col_integer(), 
                                             birth_date = col_datetime(format = "%Y-%m-%d"), 
                                             age = col_integer(), degree = col_integer(), 
                                             incumbent = col_integer(), valid_votes = col_integer(), 
                                             total_votes = col_integer(), electorate = col_integer(), 
                                             pop = col_integer(), vote = col_integer(), 
                                             vote_margin = col_integer(), tier = col_integer(), 
                                             experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                             defect_period = col_integer(), president = col_integer(), 
                                             vice_president = col_integer()))

defection_3_ext <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_session_type_3.csv", 
                            col_types = cols(...1 = col_integer(), 
                                             name_id = col_integer(), session = col_integer(), 
                                             term = col_integer(), sex = col_integer(), 
                                             onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                             leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                             party_num = col_integer(), party_group_num = col_integer(), 
                                             birth_date = col_datetime(format = "%Y-%m-%d"), 
                                             age = col_integer(), degree = col_integer(), 
                                             incumbent = col_integer(), valid_votes = col_integer(), 
                                             total_votes = col_integer(), electorate = col_integer(), 
                                             pop = col_integer(), vote = col_integer(), 
                                             vote_margin = col_integer(), tier = col_integer(), 
                                             experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                             defect_period = col_integer(), president = col_integer(), 
                                             vice_president = col_integer()))

defection_1_ext_time <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_time_type_1.csv", 
                            col_types = cols(...1 = col_integer(), 
                                             name_id = col_integer(), time = col_datetime(format = "%Y-%m-%d"), 
                                             term = col_integer(), sex = col_integer(), 
                                             onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                             leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                             party_num = col_integer(), party_group_num = col_integer(), 
                                             birth_date = col_datetime(format = "%Y-%m-%d"), 
                                             age = col_integer(), degree = col_integer(), 
                                             incumbent = col_integer(), valid_votes = col_integer(), 
                                             total_votes = col_integer(), electorate = col_integer(), 
                                             pop = col_integer(), vote = col_integer(), 
                                             vote_margin = col_integer(), tier = col_integer(), 
                                             experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                             defect_period = col_integer(), president = col_integer(), 
                                             vice_president = col_integer()))

defection_2_ext_time <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_time_type_2.csv", 
                                 col_types = cols(...1 = col_integer(), 
                                                  name_id = col_integer(), time = col_datetime(format = "%Y-%m-%d"), 
                                                  term = col_integer(), sex = col_integer(), 
                                                  onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                                  leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                                  party_num = col_integer(), party_group_num = col_integer(), 
                                                  birth_date = col_datetime(format = "%Y-%m-%d"), 
                                                  age = col_integer(), degree = col_integer(), 
                                                  incumbent = col_integer(), valid_votes = col_integer(), 
                                                  total_votes = col_integer(), electorate = col_integer(), 
                                                  pop = col_integer(), vote = col_integer(), 
                                                  vote_margin = col_integer(), tier = col_integer(), 
                                                  experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                                  defect_period = col_integer(), president = col_integer(), 
                                                  vice_president = col_integer()))

defection_3_ext_time <- read_csv("Thesis/recall_in_taiwan/data/gazette_analysis/defection_by_time_type_3.csv", 
                                 col_types = cols(...1 = col_integer(), 
                                                  name_id = col_integer(), time = col_datetime(format = "%Y-%m-%d"), 
                                                  term = col_integer(), sex = col_integer(), 
                                                  onboardDate = col_datetime(format = "%Y-%m-%d"), 
                                                  leaveDate = col_datetime(format = "%Y-%m-%d"), 
                                                  party_num = col_integer(), party_group_num = col_integer(), 
                                                  birth_date = col_datetime(format = "%Y-%m-%d"), 
                                                  age = col_integer(), degree = col_integer(), 
                                                  incumbent = col_integer(), valid_votes = col_integer(), 
                                                  total_votes = col_integer(), electorate = col_integer(), 
                                                  pop = col_integer(), vote = col_integer(), 
                                                  vote_margin = col_integer(), tier = col_integer(), 
                                                  experience = col_integer(), defect_date = col_datetime(format = "%Y-%m-%d"), 
                                                  defect_period = col_integer(), president = col_integer(), 
                                                  vice_president = col_integer()))









defection_1_ext <- 
  defection_1_ext %>% 
  filter(tier < 3) %>% 
  filter(party == "民主進步黨")
defection_2_ext <- defection_2_ext %>% 
  filter(tier < 3) %>% 
  filter(party == "民主進步黨")
defection_3_ext <- defection_3_ext %>% 
  filter(tier < 3) %>% 
  filter(party == "民主進步黨")



defection_1_ext$period <- defection_1_ext %>%
  data.table::frank(term, session, ties.method = "dense")

defection_2_ext$period <- defection_2_ext %>%
  data.table::frank(term, session, ties.method = "dense")

defection_3_ext$period <- defection_3_ext %>%
  data.table::frank(term, session, ties.method = "dense")


defection_1_ext <- defection_1_ext %>% 
  mutate(treated_a = tier == 1 & period > 9)
defection_2_ext <- defection_2_ext %>% 
  mutate(treated_a = tier == 1 & period > 9)
defection_3_ext <- defection_3_ext %>% 
  mutate(treated_a = tier == 1 & period > 9)

defection_1_ext <- defection_1_ext %>% 
  mutate(treated_b = tier == 1 & period > 10)
defection_2_ext <- defection_2_ext %>% 
  mutate(treated_b = tier == 1 & period > 10)
defection_3_ext <- defection_3_ext %>% 
  mutate(treated_b = tier == 1 & period > 10)

defection_1_ext <- defection_1_ext %>% 
  mutate(treated_c = tier == 1 & period > 11)
defection_2_ext <- defection_2_ext %>% 
  mutate(treated_c = tier == 1 & period > 11)
defection_3_ext <- defection_3_ext %>% 
  mutate(treated_c = tier == 1 & period > 11)



clfe_a1 <- feols(defect_rate ~ treated_a | tier + period,
              data = defection_1_ext)
clfe_a2 <- feols(defect_rate ~ treated_a | tier + period,
                 data = defection_2_ext)
clfe_a3 <- feols(defect_rate ~ treated_a | tier + period,
                 data = defection_3_ext)
clfe_b1 <- feols(defect_rate ~ treated_b | tier + period,
                 data = defection_1_ext)
clfe_b2 <- feols(defect_rate ~ treated_b | tier + period,
                 data = defection_2_ext)
clfe_b3 <- feols(defect_rate ~ treated_b | tier + period,
                 data = defection_3_ext)
clfe_c1 <- feols(defect_rate ~ treated_c | tier + period,
                 data = defection_1_ext)
clfe_c2 <- feols(defect_rate ~ treated_c | tier + period,
                 data = defection_2_ext)
clfe_c3 <- feols(defect_rate ~ treated_c | tier + period,
                 data = defection_3_ext)
table_1 <- msummary(
  list(clfe_a1, clfe_a2, clfe_a3),
              # list(clfe_a1, clfe_a2, clfe_a3, 
              # clfe_b1, clfe_b2, clfe_b3,
              # clfe_c1, clfe_c2, clfe_c3
              # ),
              stars = c('*' = .1, '**' = .05, '***' = .01),
              fmt = fmt_sprintf("%.4f"),
              output = "table.docx"
              )




test_defection_ext_a1 <- defection_1_ext %>% 
  filter(period < 10) %>% 
  mutate(fake_treated_8 = tier == 1 & period > 8) %>% 
  mutate(fake_treated_7 = tier == 1 & period > 7) %>% 
  mutate(fake_treated_6 = tier == 1 & period > 6) %>% 
  mutate(fake_treated_5 = tier == 1 & period > 5) %>% 
  mutate(fake_treated_4 = tier == 1 & period > 4) %>% 
  mutate(fake_treated_3 = tier == 1 & period > 3) %>% 
  mutate(fake_treated_2 = tier == 1 & period > 2) %>% 
  mutate(fake_treated_1 = tier == 1 & period > 1)
fake_8 <- feols(defect_rate ~ fake_treated_8 | tier + period,
                 data = test_defection_ext_a1)
fake_7 <- feols(defect_rate ~ fake_treated_7 | tier + period,
                data = test_defection_ext_a1)
fake_6 <- feols(defect_rate ~ fake_treated_6 | tier + period,
                data = test_defection_ext_a1)
fake_5 <- feols(defect_rate ~ fake_treated_5 | tier + period,
                data = test_defection_ext_a1)
fake_4 <- feols(defect_rate ~ fake_treated_4 | tier + period,
                data = test_defection_ext_a1)
fake_3 <- feols(defect_rate ~ fake_treated_3 | tier + period,
                data = test_defection_ext_a1)
fake_2 <- feols(defect_rate ~ fake_treated_2 | tier + period,
                data = test_defection_ext_a1)
fake_1 <- feols(defect_rate ~ fake_treated_1 | tier + period,
                data = test_defection_ext_a1)
well <- msummary(list(fake_1, fake_2, fake_3, 
              fake_4, fake_5, fake_6,
              fake_7, fake_8), stars = c('*' = .1, '**' = .05, '***' = .01),
              output = "placebo_x.docx")

placebo_effects <- data.frame(
  time = c("Session 1", "Session 2", "Session 1", "Session 2"),
  group = c("Placebo 1", "Placebo 1", "Placebo 2", "Placebo 2"),
  effect = c(coef(fake_1)[3], coef(fake_1)[4], 
             coef(fake_2)[3], coef(fake_22)[4])
)
ggplot(placebo_effects, aes(x = time, y = effect, fill = group)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme(legend.position = "top")



coefplot(well)

test_defection_ext_a2 <- defection_2_ext %>% 
  filter(period < 10) %>% 
  mutate(fake_treated_8 = tier == 1 & period > 8) %>% 
  mutate(fake_treated_7 = tier == 1 & period > 7) %>% 
  mutate(fake_treated_6 = tier == 1 & period > 6) %>% 
  mutate(fake_treated_5 = tier == 1 & period > 5) %>% 
  mutate(fake_treated_4 = tier == 1 & period > 4) %>% 
  mutate(fake_treated_3 = tier == 1 & period > 3) %>% 
  mutate(fake_treated_2 = tier == 1 & period > 2) %>% 
  mutate(fake_treated_1 = tier == 1 & period > 1)
fake_8_1 <- feols(defect_rate ~ fake_treated_8 | tier + period,
                data = test_defection_ext_a2)
fake_7_1 <- feols(defect_rate ~ fake_treated_7 | tier + period,
                data = test_defection_ext_a2)
fake_6_1 <- feols(defect_rate ~ fake_treated_6 | tier + period,
                data = test_defection_ext_a2)
fake_5_1 <- feols(defect_rate ~ fake_treated_5 | tier + period,
                data = test_defection_ext_a2)
fake_4_1 <- feols(defect_rate ~ fake_treated_4 | tier + period,
                data = test_defection_ext_a2)
fake_3_1 <- feols(defect_rate ~ fake_treated_3 | tier + period,
                data = test_defection_ext_a2)
fake_2_1 <- feols(defect_rate ~ fake_treated_2 | tier + period,
                data = test_defection_ext_a2)
fake_1_1 <- feols(defect_rate ~ fake_treated_1 | tier + period,
                data = test_defection_ext_a2)
well_1 <- msummary(list(fake_1_1, fake_2_1, fake_3_1, 
                      fake_4_1, fake_5_1, fake_6_1,
                      fake_7_1, fake_8_1), stars = c('*' = .1, '**' = .05, '***' = .01),
                   output = "placebo_2.docx")

test_defection_ext_a3 <- defection_3_ext %>% 
  filter(period < 10) %>% 
  mutate(fake_treated_8 = tier == 1 & period > 8) %>% 
  mutate(fake_treated_7 = tier == 1 & period > 7) %>% 
  mutate(fake_treated_6 = tier == 1 & period > 6) %>% 
  mutate(fake_treated_5 = tier == 1 & period > 5) %>% 
  mutate(fake_treated_4 = tier == 1 & period > 4) %>% 
  mutate(fake_treated_3 = tier == 1 & period > 3) %>% 
  mutate(fake_treated_2 = tier == 1 & period > 2) %>% 
  mutate(fake_treated_1 = tier == 1 & period > 1)
fake_8_2 <- feols(defect_rate ~ fake_treated_8 | tier + period,
                  data = test_defection_ext_a3)
fake_7_2 <- feols(defect_rate ~ fake_treated_7 | tier + period,
                  data = test_defection_ext_a3)
fake_6_2 <- feols(defect_rate ~ fake_treated_6 | tier + period,
                  data = test_defection_ext_a3)
fake_5_2 <- feols(defect_rate ~ fake_treated_5 | tier + period,
                  data = test_defection_ext_a3)
fake_4_2 <- feols(defect_rate ~ fake_treated_4 | tier + period,
                  data = test_defection_ext_a3)
fake_3_2 <- feols(defect_rate ~ fake_treated_3 | tier + period,
                  data = test_defection_ext_a3)
fake_2_2 <- feols(defect_rate ~ fake_treated_2 | tier + period,
                  data = test_defection_ext_a3)
fake_1_2 <- feols(defect_rate ~ fake_treated_1 | tier + period,
                  data = test_defection_ext_a3)
well_2 <- msummary(list(fake_1_2, fake_2_2, fake_3_2, 
                        fake_4_2, fake_5_2, fake_6_2,
                        fake_7_2, fake_8_2), stars = c('*' = .1, '**' = .05, '***' = .01),
                   output = "placebo_3.docx",
                   fmt = fmt_sprintf("%.2f"))



dynamic_defection_1_ext <- 
  defection_1_ext %>% 
  mutate(tier_2 = tier == 2)
clfe_1 <- feols(defect_rate ~ i(period, tier_2) | 
                tier + period, data = dynamic_defection_1_ext)
msummary(clfe_1)
# And use coefplot() for a graph of effects
coefplot(clfe_1)


defection_2_ext <- defection_2_ext %>% 
  mutate(treated_c = tier == 1 & period > 11)
defection_3_ext <- defection_3_ext %>% 
  mutate(treated_c = tier == 1 & period > 11)


defection_1_ext_time_mean <- defection_1_ext_time %>% 
  group_by(time, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

attach(defection_1_ext_time_mean)
a <- ggplot(defection_1_ext_time_mean, aes(x = time, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_1_ext_time_mean)

defection_2_ext_time_mean <- defection_2_ext_time %>% 
  group_by(time, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

attach(defection_2_ext_time_mean)
a <- ggplot(defection_2_ext_time_mean, aes(x = time, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_2_ext_time_mean)

defection_3_ext_time_mean <- defection_3_ext_time %>% 
  group_by(time, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)


attach(defection_3_ext_time_mean)
a <- ggplot(defection_3_ext_time_mean, aes(x = time, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_3_ext_time_mean)


defection_1_ext_mean <- defection_1_ext %>% 
  group_by(period, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

defection_1_ext_num <- defection_1_ext %>% 
  group_by(period, tier) %>% 
  summarize(count = sum(defect_rate > 0)) %>% 
  filter(tier < 3)

attach(defection_1_ext_num)
a <- ggplot(defection_1_ext_num, aes(x = period, y = as.integer(count), color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
 detach(defection_1_ext_num)

defection_1_num <- defection_1 %>% 
  group_by(term, tier) %>% 
  summarize(count = sum(defect_rate > 0)) %>% 
  filter(tier < 3)

attach(defection_1_num)
a <- ggplot(defection_1_num, aes(x = term, y = as.integer(count), color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_1_num)

defection_2_num <- defection_2 %>% 
  group_by(term, tier) %>% 
  summarize(count = sum(defect_rate > 0)) %>% 
  filter(tier < 3)

attach(defection_2_num)
a <- ggplot(defection_2_num, aes(x = term, y = as.integer(count), color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_2_num)

defection_3_num <- defection_3 %>% 
  group_by(term, tier) %>% 
  summarize(count = sum(defect_rate > 0)) %>% 
  filter(tier < 3)

attach(defection_3_num)
a <- ggplot(defection_3_num, aes(x = term, y = as.integer(count), color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_3_num)




defection_2_ext_mean <- defection_2_ext %>% 
  group_by(period, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

defection_3_ext_mean <- defection_3_ext %>% 
  group_by(period, tier) %>% 
  summarise(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

defection_1_mean <- defection_1 %>% 
  group_by(term, tier) %>% 
  summarize(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

attach(defection_1_mean)
a <- ggplot(defection_1_mean, aes(x = term, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_1_mean)

defection_2_mean <- defection_2 %>% 
  group_by(term, tier) %>% 
  summarize(avg = mean(defect_rate) ) %>% 
  filter(tier < 3)

attach(defection_2_mean)
a <- ggplot(defection_2_mean, aes(x = term, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(term) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_2_mean)

attach(defection_3_mean)
a <- ggplot(defection_3_mean, aes(x = term, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) )  )
a + b + d
detach(defection_3_mean)

x_ticks_1 <-
  c("9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7", "9.8",
    "10.1", "10.2", "10.3", "10.4", "10.5", "10.6")
x_ticks <- 
  c("Session 1, Term 9",
    "Session 2", 
    "Session 3", 
    "Session 4", 
    "Session 5", 
    "Session 6", 
    "Session 7", 
    "Session 8", 
    "Session 1, Term 10",
    "Session 2",
    "Session 3",
    "Session 4",
    "Session 5",
    "Session 6"
    )

attach(defection_1_ext_mean)
a <- ggplot(defection_1_ext_mean, aes(x = period, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier), label = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) ), name = "Tier"  )
e <- geom_vline(xintercept=10,linetype=4)
graph_1 <- a + b + d + e +
  ylab("Defection Rate") +
  labs(title = "Type-I Defection Rate Trends", color = "Tier", labels = c("Nominal", "Party"))+
  scale_color_manual(labels = c("Nominal", "Party")
                     ,values = cbp1)+
  scale_x_discrete(name ="Session", limits = c(1:14), labels=x_ticks_1)
detach(defection_1_ext_mean)
attach(defection_2_ext_mean)
a <- ggplot(defection_2_ext_mean, aes(x = period, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier), label = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) ), name = "Tier"  )
e <- geom_vline(xintercept=10,linetype=4)
graph_2 <- a + b + d + e +
  ylab("Defection Rate") +
  labs(title = "Type-II Defection Rate Trends", color = "Tier", labels = c("Nominal", "Party"))+
  scale_color_manual(labels = c("Nominal", "Party")
                     ,values = cbp1)+
  scale_x_discrete(name ="Session", limits = c(1:14), labels=x_ticks_1)
detach(defection_2_ext_mean)
attach(defection_3_ext_mean)
a <- ggplot(defection_3_ext_mean, aes(x = period, y = avg, color = factor(tier) ) )
b <- geom_point(color = factor(tier), label = factor(tier) )
c <- geom_text(aes(label = tier ) ) 
d <- geom_line(aes(group = tier, color = factor(tier) ), name = "Tier"  )
e <- geom_vline(xintercept=10,linetype=4)
graph_3 <- a + b + d + e +
  ylab("Defection Rate") +
  labs(title = "Type-III Defection Rate Trends", color = "Tier", labels = c("Nominal", "Party"))+
  scale_color_manual(labels = c("Nominal", "Party")
                     ,values = cbp1)+
  scale_x_discrete(name ="Session", limits = c(1:14), labels=x_ticks_1)
detach(defection_3_ext_mean)

graph_1 / graph_2 / graph_3 +
  plot_annotation(caption = "Note: For values in session, digits before the . stands for the term and those after the . session order. E.g., 10.2 stands for session 2 of the 10th term.")
