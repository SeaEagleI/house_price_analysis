houses <- read.csv('C:\\Users\\Messy XUE\\Desktop\\ershoufang_preprocessed.csv',sep=',',header=T)
library(ggplot2)
library(Hmisc)
library(car)
library(caret)

names(houses)
dim(houses)


#各区二手房单价
avg_price_by_region <- aggregate(houses$"单价.元.平.",by=list(houses$"区域"),FUN=mean)
plot_avg_price_by_region <- ggplot(data=avg_price_by_region,aes(x=reorder(Group.1,-x),y=x,group=1))+
  geom_area(fill='lightgreen')+
  geom_line(colour = 'steelblue', size = 2)+
  geom_point()+
  ylab('均价/万')
plot_avg_price_by_region


#各商圈二手房单价
avg_price_by_business_district <- aggregate(houses$"单价.元.平.",by=list(houses$"商圈"),FUN=mean)
plot_avg_price_by_business_district <- ggplot(data=avg_price_by_business_district,aes(x=reorder(Group.1,-x),y=x,group=1))+
  geom_area(fill='lightgreen')+
  geom_line(colour = 'steelblue', size = 2)+
  geom_point()+
  ylab('均价/万')
plot_avg_price_by_business_district


#各小区二手房均价
avg_price_by_resident_district <- aggregate(houses$"单价.元.平.",by=list(houses$"小区"),FUN=mean)
plot_avg_price_by_resident_district <- ggplot(data=avg_price_by_resident_district,aes(x=reorder(Group.1,-x),y=x,group=1))+
  geom_area(fill='lightgreen')+
  geom_line(colour = 'steelblue', size = 2)+
  geom_point()+
  ylab('均价/万')
plot_avg_price_by_resident_district


#查看户型情况
type_freq <- data.frame(table(houses$"房屋户型"))
plot_house_type <- ggplot(data=type_freq,aes(x=reorder(Var1,-Freq),y=Freq))+
  geom_bar(stat='identity',fill='steelblue')+
  theme(axis.text.x = element_text(angle = 30,vjust = 0.5))+
  xlab('户型')+
  ylab('套数')
plot_house_type
#统计各户型个数
type_count <- aggregate(houses$"房屋户型", by = list(houses$"房屋户型"), FUN = length)
type_count
# 把低于一千套的房型设置为其他
type <- c('2室1厅1卫', '1室1厅1卫', '3室1厅1卫',
          '3室2厅2卫', '3室1厅2卫', '2室2厅1卫',
          '1室0厅1卫', '2室1厅2卫', '4室2厅2卫',
          '3室2厅1卫', '2室2厅2卫', '4室2厅3卫')

houses$type.new <- ifelse(houses$"房屋户型" %in% type,as.character(houses$"房屋户型"),'其他')
type_freq <- data.frame(table(houses$type.new))
# 重新绘图
plot_house_type_new <- ggplot(data = type_freq, mapping = aes(x = reorder(Var1, -Freq),y = Freq)) + 
  geom_bar(stat = 'identity', fill = 'steelblue') + 
  theme(axis.text.x  = element_text(angle = 30, vjust = 0.5)) + 
  xlab('户型') + ylab('套数')
plot_house_type_new

houses<-na.omit(houses)


# 模型构建
tot.wssplot <- function(data,nc,seed=1234){
  # 计算距离的平方和
  tot.wss <- (nrow(data)-1) * sum(apply(data,2,var))
  for(i in 2:nc){
    set.seed(seed)
    tot.wss[i] <- kmeans(data,centers = i,iter.max = 100)$tot.withinss
  }
  plot(1:nc,tot.wss,type='b',xlab = 'Number of Cluster',
       ylab = 'Within groups sum of squares',col='blue',lwd=2,
       main='choose best clusters')
}
# 找出判断聚类的三个主要的指标
stander <- data.frame(scale(houses[,c("建筑面积...","评估价" ,"单价.元.平.")]))
# 做出聚类个数图
tot.wssplot(stander,15)


#聚类
set.seed(1234)
clust <- kmeans(x=stander,centers = 6,iter.max = 100)
table(clust$cluster)
# 查看每个户型的平均面积
aggregate(houses$"建筑面积...",list(houses$type.new),FUN=mean)
# 比较每个类中的面积,单价,每平米价格
#aggregate(cbind(houses$"建筑面积...",houses$"评估价" ,houses$"单价.元.平."),list(clust$cluster),FUN=mean)
aggregate(houses[c("建筑面积...","评估价" ,"单价.元.平.")],list(clust$cluster),FUN=mean)





#聚类散点图?????(结果有误)
clust_plot <- ggplot(data=houses[,c("建筑面积...","评估价" ,"单价.元.平.")],aes(x="建筑面积...",y="单价.元.平.",color=factor(clust$cluster)))+
  geom_point(pch=20,size=3)+
  scale_color_manual(values = c('red','blue','green','black','orange','yellow'))
clust_plot


#建筑时间替换
# 自定义众数函数
stat.mode <- function(x, rm.na = TRUE){
  if (rm.na == TRUE){
    y = x[!is.na(x)]
  }
  res = names(table(y))[which.max(table(y))]
  return(res)
}
# 自定义函数，实现分组替补
my_impute <- function(data, category.col = NULL, 
                      miss.col = NULL, method = stat.mode){
  impute.data = NULL
  for(i in as.character(unique(data[,category.col]))){
    sub.data = subset(data, data[,category.col] == i)
    sub.data[,miss.col] = impute(sub.data[,miss.col], method)
    impute.data = c(impute.data, sub.data[,miss.col])
  }
  data[,miss.col] = impute.data
  return(data)
}
# 将建筑时间中空白字符串转换为缺失值
#houses$"建筑年代"[houses$"建筑年代" == ""] <- 2015
#分组替补缺失值，并对数据集进行变量筛选

final_house <- subset(houses,select = c("type.new","所在楼层","建筑面积...","评估价","单价.元.平." ,"建筑年代"))
#构建新字段builtdate2now，即建筑时间与当前2016年的时长
final_house <- transform(final_house, builtdate2now = 2021-as.integer(substring(as.character(final_house$"建筑年代"),1,4)))
#删除原始的建筑时间这一字段
final_house <- final_house[-c(6)]


#对final_house聚类
# 模型构建
tot.wssplot <- function(data,nc,seed=1234){
  # 计算距离的平方和
  tot.wss <- (nrow(data)-1) * sum(apply(data,2,var))
  for(i in 2:nc){
    set.seed(seed)
    tot.wss[i] <- kmeans(data,centers = i,iter.max = 100)$tot.withinss
  }
  plot(1:nc,tot.wss,type='b',xlab = 'Number of Cluster',
       ylab = 'Within groups sum of squares',col='blue',lwd=2,
       main='choose best clusters')
}
# 找出判断聚类的三个主要的指标
stander <- data.frame(scale(final_house[,c("建筑面积...","评估价" ,"单价.元.平.")]))
# 做出聚类个数图
tot.wssplot(stander,15)


#对final_house聚类
set.seed(1234)
clust <- kmeans(x=stander,centers = 6,iter.max = 100)
table(clust$cluster)
# 查看每个户型的平均面积
aggregate(final_house$"建筑面积...",list(final_house$type.new),FUN=mean)
# 比较每个类中的面积,单价,每平米价格
#aggregate(cbind(houses$"建筑面积...",houses$"评估价" ,houses$"单价.元.平."),list(clust$cluster),FUN=mean)
aggregate(final_house[,3:5],list(clust$cluster),FUN=mean)




#？聚类散点图（依然有问题）
clust_plot <- ggplot(data=final_house[,3:5],aes(x="建筑面积...",y="单价.元.平.",color=factor(clust$cluster)))+
  geom_point(pch=20,size=3)+
  scale_color_manual(values = c('red','blue','green','black','orange','yellow'))
clust_plot

#建模(caret包导入失败，，，dummyVars函数没办法调用)
#将类别变量变成因子类型
final_house$"所在楼层" <- factor(final_house$"所在楼层")
final_house$"type.new" <- factor(final_house$"type.new")
final_house$clsuter <- factor(clust$cluster)
# 选择出所有的因子变量
factors <- names(final_house)[sapply(final_house, class)=='factor']
formal <- f <- as.formula(paste('~',paste(factors,collapse = '+')))
formal
dummy <- dummyVars(formula = formal,data=final_house)
pred <- predict(dummy,newdata=final_house)
head(pred)