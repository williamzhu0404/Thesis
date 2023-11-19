library(reticulate)
library(this.path)


library(haven)

setwd(here())




source_python("pickle_reader.py")
pickle_data <- read_pickle_file("C:/tsa/dataset.pickle")

Rollcall_vote_merge_5_8_V_10 <- read_dta("Thesis/recall_in_taiwan/data/liao_2022_data/Rollcall vote merge_5-8_V.10.dta")




