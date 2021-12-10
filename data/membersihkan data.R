library(jsonlite)

kode <- fromJSON("kode_negara_lengkap.json")

write.csv(kode, "kode_negara_lengkap.csv")

kode <- kode[c('name', 'alpha-3', 'region', 'sub-region')]
colnames(kode) <- c('name', 'kode_negara', 'region', 'sub-region')

################
library(tidyverse)
df <- read.csv("produksi_minyak_mentah (asli).csv")

`%notin%` <- Negate(`%in%`)

df <- df %>%
  filter(kode_negara %notin% c('WLD', 'G20', 'OECD', 'OEU')
  )

write.csv(df, "produksi_minyak_mentah.csv")

#################
df_lengkap <- inner_join(df, kode, by="kode_negara")
write.csv(df_lengkap, "produksi_minyak_mentah_lengkap.csv")
