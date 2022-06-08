library(dplyr)
library(tidyr)

# First, you need to have the devtools package installed
install.packages("devtools")
# now, install the vdemdata package directly from GitHub
devtools::install_github("vdeminstitute/vdemdata")


library(vdemdata)

vdem_2020_now <- vdem %>% filter(year > 2019)
identifier_list <- 
  c("country_name", 
    "country_id", 
    "country_text_id")
vdem_high_level_indices_list <- 
  c("v2x_polyarchy", 
    "v2x_libdem", 
    "v2x_partipdem", 
    "v2x_delibdem", 
    "v2x_egaldem")
vdem_regime_of_the_world <- 
  c("v2x_regime", 
    "v2x_regime_amb")
var_names <- c("year",
               identifier_list, 
               vdem_high_level_indices_list, 
               vdem_regime_of_the_world
               )  
E_DEM <- 2#the score for electoral democracy in v2x_regime
pt_est_dems <- vdem_2020_now %>% filter(v2x_regime >= E_DEM)
pt_est_dems_names <- distinct(select(pt_est_dems, country_name))
vdem_2020_now_essential <- 
  pt_est_dems %>% 
  select(one_of(var_names) )

LEN <- 2

test<-
  vdem_2020_now_essential %>% 
  group_by(country_id) %>% 
  summarise(experience = n()) %>% 
  filter(experience >= LEN)

