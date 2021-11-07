# 贝壳找房API爬虫

## 目标城市

- 目标城市：北京
- 城市编号：110000
- 城市缩写：bj

## 相关网址
- 贝壳找房：https://www.ke.com
- 北京二手房：https://bj.ke.com/ershoufang/
- 北京租房：https://bj.zu.ke.com/zufang/
- 北京新房：https://bj.fang.ke.com/loupan/

## 已实现功能

|                             功能                             | 爬取房源数 |         网站实时房源数（1107）         | API数据重复性 |     网站数据重复性     | 爬取结果去重 |
| :----------------------------------------------------------: | :--------: | :------------------------------------: | :-----------: | :--------------------: | :----------: |
| [获取二手房房源](https://github.com/SeaEagleI/shell_crawler/blob/master/ershoufang.py) |   91136    | [91136](https://bj.ke.com/ershoufang/) |    无重复     |         无重复         |     ---      |
| [获取租房房源](https://github.com/SeaEagleI/shell_crawler/blob/master/zufang.py) |   36069    | [38069](https://bj.zu.ke.com/zufang/)  |    有重复     |          ---           |    已去重    |
| [获取新房房源](https://github.com/SeaEagleI/shell_crawler/blob/master/newhouse.py) |    261     | [261](https://bj.fang.ke.com/loupan/)  |    有重复     | 有重复（存在一房多挂） |    未去重    |

### 说明
- 运行相应python程序即可在data目录下生成格式为json的房源信息文件，文件中房源信息数如上表所示。
- 以上房源数仅为程序2021年11月7日0时0分获得的结果，而贝壳网的房源数据是持续变化的，重新运行程序即可得到包含最新房源数量和信息的文件。
- 租房API提供数据存在较多冗余，使用"house_code"字段对房源去重后为36069条，与网站实时结果差2k左右。原因具体是以下哪种仍有待研究，但不影响后期对数据的使用和分析：
（1）API提供的数据不完整；
（2）贝壳网租房信息本身存在冗余（如一房多挂）。

## TODO List
### Python代码转R
- https://github.com/Mounment/R-Project/tree/master/上海二手房分析

### 数据预处理及分析
- https://github.com/ideaOzy/data_analysis
- https://blog.51cto.com/u_15168725/2708108
- https://zhuanlan.zhihu.com/p/359589517

## 参考
- https://www.zhihu.com/question/443457100/answer/1721778654
- https://github.com/CaoZ/Fast-LianJia-Crawler
- https://zhuanlan.zhihu.com/p/370244126

## 声明
本项目仅供学习交流使用，严禁使用本项目作商业用途，违者后果自负。
