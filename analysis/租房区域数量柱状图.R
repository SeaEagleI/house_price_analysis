zufang <- read.csv('zufang.csv')
library(tidyverse)
library(ggplot2)
zufang1 <- zufang %>% mutate(number = X+1)
zufang1 <- zufang1 %>% select(number, district_name) 
zufang1 <- data.frame(zufang1)
#zufang1 %>% ggplot(district_name,aes(x=district_name)) +geom_line()
#ggplot(zufang1, aes(x= as.character(length), y=district_name)) + geom_line()
library(ggthemes)
ggplot(zufang1, aes(x= district_name)) + geom_bar() +xlab("区域") + ylab("数量") + ggtitle("北京各区域租房数量图") +
  theme_economist() 
zufang <- read.csv('zufang.csv')
library(tidyverse)
library(ggplot2)
zufang1 <- zufang %>% mutate(number = X+1)
zufang1 <- zufang1 %>% select(number, district_name) 
zufang1 <- data.frame(zufang1)
#zufang1 %>% ggplot(district_name,aes(x=district_name)) +geom_line()
#ggplot(zufang1, aes(x= as.character(length), y=district_name)) + geom_line()
#fill = "#E1BF8C
ggplot(zufang1, aes(x= district_name)) + geom_bar(fill = "#E1BF8C") +
xlab("区域") + ylab("数量") + ggtitle("北京各区域租房数量图") +
  theme_classic() 
                                                  

