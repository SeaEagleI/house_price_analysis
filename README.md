# 基于贝壳找房网的北京房源爬虫与房价分析可视化

## 目标城市信息

- 北京（城市编号110000，城市缩写bj）

## Part I: 数据获取（API爬虫）

### 数据源网址

- 贝壳找房：https://www.ke.com
- 北京二手房：https://bj.ke.com/ershoufang/
- 北京租房：https://bj.zu.ke.com/zufang/

### 爬虫代码及爬取结果展示

|                             功能                             | 爬取耗时 | 爬取房源数 |         网站实时房源数（1107）         | API数据重复性 |     网站数据重复性     | 爬取结果去重 |
| :----------------------------------------------------------: | :----------------: | :--------: | :------------------------------------: | :-----------: | :--------------------: | :----------: |
| [获取二手房房源](https://github.com/SeaEagleI/house_price_analysis/blob/master/ershoufang.py) | 约40分钟           |   91136    | [91136](https://bj.ke.com/ershoufang/) |    无重复     |         无重复         |     ---      |
| [获取租房房源](https://github.com/SeaEagleI/house_price_analysis/blob/master/zufang.py) | 约40分钟           |   36069    | [38069](https://bj.zu.ke.com/zufang/)  |    有重复     |          ---           |    已去重    |
| [获取新房房源](https://github.com/SeaEagleI/house_price_analysis/blob/master/newhouse.py) | 约10秒           |    261     | [261](https://bj.fang.ke.com/loupan/)  |    有重复     | 有重复（存在一房多挂） |    未去重    |

### 说明
- 运行相应python程序即可在data目录下生成格式为json的房源信息文件，文件中房源信息数如上表所示。
- 以上房源数仅为程序2021年11月7日0时0分获得的结果，而贝壳网的房源数据是持续变化的，重新运行程序即可得到包含最新房源数量和信息的文件。
- 租房API提供数据存在较多冗余，使用"house_code"字段对房源去重后为36069条，与网站实时结果差2k左右。原因具体是以下哪种仍有待研究，但不影响后期对数据的使用和分析：
    1. API提供的数据不完整；
    2. 贝壳网租房信息本身存在冗余（如一房多挂）。
- 项目全部数据见[wps共享文件夹](https://kdocs.cn/join/gi5qoxj)，链接永久有效。（涉及数据量较大，git限制上传的单个文件大小上限是50MB）

### 爬虫代码参考
- https://www.zhihu.com/question/443457100/answer/1721778654
- https://github.com/CaoZ/Fast-LianJia-Crawler
- https://zhuanlan.zhihu.com/p/370244126

## Part II: 数据预处理

- 文件格式转换：[将爬取的json文件转为csv](https://github.com/SeaEagleI/house_price_analysis/blob/master/preprocess/json2csv.py)
- 数据整理：[删除冗余或用不到的列，对列进行整理、拆分与合并，并重命名列名](https://github.com/SeaEagleI/house_price_analysis/blob/master/preprocess/ershoufang.py)

## Part III: 数据分析及可视化

### TODO List
1. 所有房源分析（哪些类型/特点的房子最多: 楼层？价格？房屋类型 ==> 词云/词频统计）
2. 区域/商圈间比较（房价、房源数 ==> 区域热力图）
3. 房源类型分布与区位的关系（比如学区房倾向于都是小房子？）
4. 各因素对房价的影响（区域、商圈、学区、楼层、房屋面积、建房时间？）
5. 二手房、租房、新房间的横向对比（二手房交易频繁的区域租房房源也是最多吗？有没有房子既是二手房也是出租房？）

### 分析及可视化参考
- https://github.com/ideaOzy/data_analysis
- https://blog.51cto.com/u_15168725/2708108
- https://zhuanlan.zhihu.com/p/359589517

## Part IV: Case Study

### TODO List
1. 不同总价分别适合购买哪种学区房/非学区房？（假设：全款付；范围：100w-2000w）
2. 在各个区安家分别需要多少钱？（假设：全款付；目标房价取本区所有房价的中位数）
3. 上面两个问题的结果换成只付首付分别要多少钱？（首付范围：100w-1000w；首付比例：?；现实因素：首付与总价差多少恰好能保证以后还得起？；假设：年入40w，公积金70w，10年还清？）

## 其他参考

- [ ] **Python代码转R**
  - https://github.com/Mounment/R-Project/tree/master/上海二手房分析

## 声明
本项目仅供学习交流使用，严禁使用本项目作商业用途，违者后果自负。
