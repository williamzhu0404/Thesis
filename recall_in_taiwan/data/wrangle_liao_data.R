library(dplyr)
library(tidyr)
library(ggplot2)

library(this.path)

library(haven)


setwd(here())


Roll_Call_Master <- 
  read_dta("liao_2022_data/Rollcall vote merge_5-8_V.10.dta")

tier2_order <- c("tier2", "order")
tier_order <- c("category", "order")

summary_by_tier <- 
  Roll_Call_Master %>% 
  group_by(
    across( all_of(tier_order) ) 
    ) %>% 
  summarise(avg_defect = 
              mean(
                deviall,
                na.rm = TRUE
                ) 
            )
summary_by_tier2 <- 
  Roll_Call_Master %>% 
  group_by(
    across( all_of(tier2_order) ) 
  ) %>% 
  summarise(avg_defect = 
              mean(
                deviall,
                na.rm = TRUE
              ) 
  )

tier2_1_defect <- 
  summary_by_tier2 %>% filter(tier2 == 1)
tier2_2_defect <- 
  summary_by_tier2 %>% filter(tier2 != 1)

tier2_defect_diff <- bind_cols(
  "order" = tier2_1_defect$order,
  "avg_defect_diff" = tier2_1_defect$avg_defect - tier2_2_defect$avg_defect
)

tier2_2_defect_diff_578 <- 
  tier2_defect_diff %>% 
  filter(order != 6)

# diff_tier2_1 - diff_tier2_0



# 
# difference_tier2 <-
#   summary_by_tier2 %>% 
#   group_by(tier2) %>% 
#   summarise( delta = )




tier_trend <-
summary_by_tier %>%
  ggplot( aes(x=as.integer(order), y=avg_defect, group=category, color=factor(category) )) + 
  geom_point()+ scale_color_brewer(palette="Dark2")

tier2_trend <-
  summary_by_tier2 %>%
  ggplot( aes(x=as.integer(order), y=avg_defect, group=tier2, color=factor(tier2) )) + 
  geom_point()+ scale_color_brewer(palette="Dark2")

tier2_diff_trend <-
  tier2_defect_diff %>%
  ggplot( 
    aes(
      x=as.integer(order), 
      y=avg_defect_diff 
      ) 
    )+ 
  geom_point()+ 
  geom_smooth(method='lm', 
              data = tier2_2_defect_diff_578,
              # Comment the above line to include 6th Legislative Yuan Data
              formula = y ~ x
                )

