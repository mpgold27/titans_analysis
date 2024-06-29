library(nfl4th)
library(tibble)
library(utils)

# load data
pbp <- nfl4th::load_4th_pbp(2014:2023, fast = T)
# subset onto fourth down
pbp4 <- pbp[(pbp$down==4) & (!is.na(pbp$down)),]
# save as a big dataframe
data_path <- '[INSERT YOUR PATH HERE]'
data_file <- paste0(data_path, 'fourth_down.csv.gz')
# save file
write.csv(pbp4, file=gzfile(data_file), row.names=TRUE)