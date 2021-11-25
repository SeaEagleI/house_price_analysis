library(readxl)
ershoufang <- read_xlsx('ershoufang.xlsx')
#ershoufang <- read.csv('ershoufang.csv')
library(tidyverse)
library(ggplot2)
ershoufang1 <- ershoufang %>% mutate(number = Column1+1)
ershoufang1 <- ershoufang1 %>% select(number, 区域) 
ershoufang1 <- data.frame(ershoufang1)
#ershoufang1 %>% ggplot(区域,aes(x=区域)) +geom_line()
#ggplot(ershoufang1, aes(x= as.character(length), y=区域)) + geom_line()
library(ggthemes)
ggplot(ershoufang1, aes(x= 区域)) + geom_bar() +
  xlab("区域") + ylab("数量") + ggtitle("北京各区域二手房数量图") +
  theme_economist() 
