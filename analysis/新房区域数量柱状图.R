library(readxl)
#newhouse <- read_xlsx('newhouse.xlsx')
newhouse <- read.csv('newhouse.csv')
library(tidyverse)
library(ggplot2)
newhouse1 <- newhouse %>% mutate(number = X+1)
newhouse1 <- newhouse1 %>% select(number, district_name) 
newhouse1 <- data.frame(newhouse1)
library(ggthemes)
ggplot(newhouse1, aes(x= district_name)) + geom_bar() +
  xlab("区域") + ylab("数量") + ggtitle("北京各区域新房数量图") +
  theme_economist() 
