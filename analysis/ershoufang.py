# 每个图包括: 1)数据分组、数据运算和聚合; 2)绘图（bar/parallel_bar/box/pie/scatter）
import cv2
import jieba
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from general_config import proc_file, city_abbr, na_values
from analysis.config import text_fields, cut_fields, mask_image, wordcloud_image, price_by_district_image, \
    price_by_district_box_image, unitprice_topk_communities_image
import random

task = "ershoufang"
max_total_houses = 100000
# 正常显示中文标签、负号
plt.rcParams["font.sans-serif"] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams["axes.unicode_minus"] = False
colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
rotations = [30, 45, 60]
bar_width = 0.4

# Return random color value for scatter plot
def rand_color():
    return "#" + "".join([random.choice(colorArr) for i in range(6)])


# 北京二手房词云 (wordcloud)
def paint_wordcloud(df):
    # 读入数据文件, 分词并剔除停用词
    text = df[text_fields].to_csv(header=False, index=False)
    cut_text = df[cut_fields].to_csv(header=False, index=False)
    cut_words = jieba.cut(cut_text)
    ershoufang_text = text + "\n" + " ".join(cut_words)
    print("Text Length: {}".format(len(ershoufang_text)))
    # 设置词云格式
    colors = ["white", "black"]
    for bg_color in colors:
        wordcloud = WordCloud(
            font_path="res/simhei.ttf",  # 字体，不指定就会出现乱码
            stopwords=STOPWORDS,
            background_color=bg_color,  # 背景色
            mask=cv2.imread(mask_image),  # 词云形状
            scale=8,
            max_words=1000,  # 允许最大词汇
            max_font_size=60,  # 最大号字体
        )
        # 产生词云
        wordcloud = wordcloud.generate(ershoufang_text)
        wordcloud.to_file(wordcloud_image.format("wordcloud", bg_color))
        # plt.figure("二手房词云", figsize=(30, 20), dpi=120)  # 指定所绘图名称
        # plt.imshow(wordcloud)  # 以图片的形式显示词云
        # plt.axis("off")  # 关闭图像坐标系
        # plt.show()


# 房源基本信息分布 (pie, subplots=2x3)
def paint_basic_info_distrib(df, k=8):
    # 房屋用途分布
    count_fwyt = df["房屋用途"].value_counts()[:k]
    count_other_fwyt = pd.Series({"其他": df["房屋用途"].value_counts()[k:].count()})
    count_fwyt = count_fwyt.append(count_other_fwyt)
    count_fwyt.index.name = ""
    count_fwyt.name = ""
    fig = plt.figure(figsize=(20, 20), dpi=150)
    ax = fig.add_subplot(231)
    ax.set_title("房屋用途分布", fontsize=18)
    count_fwyt.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    # 房屋户型分布
    count_fwhx = df["房屋户型"].value_counts()[:k]
    count_other_fwhx = pd.Series({"其他": df["房屋户型"].value_counts()[k:].count()})
    count_fwhx = count_fwhx.append(count_other_fwhx)
    count_fwhx.index.name = ""
    count_fwhx.name = ""
    ax = fig.add_subplot(232)
    ax.set_title("房屋户型分布", fontsize=18)
    count_fwhx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    # 装修情况分布
    count_zxqk = df["装修情况"].value_counts()
    count_zxqk.name = ""
    ax = fig.add_subplot(233)
    ax.set_title("装修情况分布", fontsize=18)
    count_zxqk.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    # 建筑类型分布
    count_jzlx = df["建筑类型"].value_counts()
    count_jzlx.name = ""
    ax = fig.add_subplot(234)
    ax.set_title("建筑类型分布", fontsize=18)
    count_jzlx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    # 房屋朝向分布
    count_fwcx = df["房屋朝向"].value_counts()[:k]
    count_other_fwcx = pd.Series({"其他": df["房屋朝向"].value_counts()[k:].count()})
    count_fwcx = count_fwcx.append(count_other_fwcx)
    ax = fig.add_subplot(235)
    ax.set_title("房源朝向分布", fontsize=18)
    count_fwcx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    # 建筑面积分布(区间)
    area_level = [0, 50, 100, 150, 200, 250, 300, 500, 100000]
    label_level = ["小于50", "50-100", "100-150", "150-200", "200-300", "300-500", "大于500"]
    jzmj_cut = pd.cut(df["建筑面积(㎡)"], area_level, labels=label_level)
    jzmj_result = jzmj_cut.value_counts()
    ax = fig.add_subplot(236)
    ax.set_ylabel("建筑面积(㎡)", fontsize=14)
    ax.set_title("建筑面积分布区间", fontsize=18)
    jzmj_result.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    plt.show()


# 各区域的房价、房源数量、平均建筑面积对比 (parallel_bar, par=3)
def paint_stats_by_district(df):
    """北京各区域二手房平均单价"""
    mean_unitprice_by_district = df["单价(元/㎡)"].groupby(df["区域"]).mean()
    mean_unitprice_by_district.index.name = ""
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("单价(元/平米)", fontsize=14)
    ax.set_title("北京各区域二手房平均单价", fontsize=18)
    mean_unitprice_by_district.plot(kind="bar", fontsize=12)
    # plt.savefig("data_ana\\picture\\mean_price.jpg")
    plt.show()
    """北京各区域二手房房源数量"""
    count_houses_by_district = df["houseCode"].groupby(df["区域"]).count()
    count_houses_by_district.index.name = ""
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("房源数量(套)", fontsize=14)
    ax.set_title("北京各区域二手房房源数量", fontsize=18)
    count_houses_by_district.plot(kind="bar", fontsize=12, grid=True)
    plt.show()
    """北京各区域二手房平均建筑面积"""
    mean_area_by_district = df["建筑面积(㎡)"].groupby(df["区域"]).mean()
    mean_area_by_district.index.name = ""
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("建筑面积(㎡)", fontsize=14)
    ax.set_title("北京各区域二手房平均建筑面积", fontsize=18)
    mean_area_by_district.plot(kind="bar", fontsize=12)
    plt.show()


# 北京二手房单价与建筑面积区位分布 (scatter)
def paint_price_area_distrib(df):
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房单价与建筑面积散点图", fontsize=18)
    # colors = ["red", "green", "blue", "yellow", "purple", "black", "pink", "orange", "cyan", ]
    # colors = [rand_color() for key in df["区域"].value_counts()]
    for k, d in df.groupby("区域"):
        d.plot.scatter(x="建筑面积(㎡)", y="单价(元/㎡)", c=rand_color(), label=k, colormap="gist_rainbow", grid=True,
                       fontsize=12,
                       ax=ax, alpha=0.4, xticks=[0, 50, 100, 150, 200, 250, 300, 400, 500, 750], xlim=[0, 1000],
                       ylim=[0, 200000])
    ax.set_xlabel("建筑面积(平米)", fontsize=14)
    ax.set_ylabel("单价(元/平米)", fontsize=14)
    plt.show()


# 北京二手房均价最高小区TopK (parallel_bar, par=2)
def paint_unitprice_topk_communities(df, k=10):
    unitprice_top_communities = df.groupby(["区域", "小区"]).mean().sort_values(["小区均价(元/㎡)"], ascending=False)[
                                    ["小区均价(元/㎡)", "建筑面积(㎡)"]][:k]
    unitprice_top_communities.index.name = ""
    x = np.arange(k)  # 柱状图在横坐标上的位置
    xtick_labels = ["\n".join(indices) for indices in unitprice_top_communities.index]
    # 绘图
    fig = plt.figure(figsize=(14, 8), dpi=150)
    ax1 = fig.add_subplot(111)
    ax1.set_title(f"北京二手房单价Top{k}小区", y=1.03, fontsize=30)
    bar1 = ax1.bar(x - bar_width / 2, unitprice_top_communities["小区均价(元/㎡)"], bar_width, color='r',
                   label="小区均价(元/㎡)")
    ax1.set_ylabel("小区均价(元/平米)", fontsize=22)
    ax1.set_yticks(np.arange(9 + 1) * 25000)
    # 显示x轴标签,即tick_label, 并调整位置使其落在两个直方图正中间
    ax1.set_xticks(x)
    ax1.set_xticklabels(xtick_labels, rotation=rotations[0], fontsize=15)
    # 第一Y轴标签、刻度颜色设置
    # ax1.yaxis.label.set_color(bar1[0].get_facecolor())
    ax1.tick_params(axis='y', labelsize=13)
    # 双Y轴设置
    ax2 = ax1.twinx()
    bar2 = ax2.bar(x + bar_width / 2, unitprice_top_communities["建筑面积(㎡)"], bar_width, color='g', label='建筑面积(㎡)')
    ax2.set_ylabel("平均建筑面积(平米)", fontsize=22)
    ax2.set_yticks(np.arange(9 + 1) * 50)
    # 第二Y轴标签、刻度颜色设置
    ax2.yaxis.label.set_color(bar2[0].get_facecolor())
    ax2.tick_params(axis='y', colors=bar2[0].get_facecolor(), labelsize=13)
    # 加数据标签
    for b in bar1:
        ax1.text(b.get_x()+bar_width/2, b.get_height(), str(int(b.get_height())), ha="center", va="bottom")
    for b in bar2:
        ax2.text(b.get_x()+bar_width/2, b.get_height(), str(int(b.get_height())), ha="center", va="bottom")
    plt.legend(handles=[bar1, bar2], fontsize=15)  # 显示图例，即label
    plt.subplots_adjust(left=0.09, bottom=0.15, right=0.92, top=0.90)  # 调整页面边距、子图间距
    # plt.grid("on")
    fig.savefig(unitprice_topk_communities_image.format(k))
    plt.show()


# 北京各区域二手房价格箱线图 (box, subplots=2x1)
def paint_price_by_district_box(df):
    # 二手房单价箱线图
    unitprice_groups_by_district = dict(sorted(list(df["单价(元/㎡)"].groupby(df["区域"])),
                                               key=lambda x: x[1].mean(), reverse=True))
    box_data = pd.DataFrame(list(range(max_total_houses)), columns=["tmp"])
    for name, group in unitprice_groups_by_district.items():
        box_data[name] = group
    del box_data["tmp"]
    fig = plt.figure(figsize=(20, 20), dpi=150)
    ax = fig.add_subplot(211)
    ax.set_title("北京各区域二手房单价箱线图", y=1.05, fontsize=45)
    ax.set_ylabel("单价(元/平米)", fontsize=22)
    box_data.plot(kind="box", fontsize=20, sym="r+", grid=True, ax=ax,
                  yticks=[10000, 20000, 30000, 40000, 50000, 100000, 150000, 180000], ylim=[0, 180000])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotations[-1])
    # 二手房总价箱线图
    totalprice_groups_by_district = dict(list(df["总价(万元)"].groupby(df["区域"])))
    box_data = pd.DataFrame(list(range(max_total_houses)), columns=["tmp"])
    for name in unitprice_groups_by_district:
        box_data[name] = totalprice_groups_by_district[name]
    del box_data["tmp"]
    ax = fig.add_subplot(212)
    ax.set_title("北京各区域二手房总价箱线图", y=1.05, fontsize=45)
    ax.set_ylabel("总价(万元)", fontsize=22)
    box_data.plot(kind="box", fontsize=20, sym="r+", grid=True, ax=ax, yticks=[0, 500, 1000, 2000, 3000, 5000, 6000],
                  ylim=[0, 6000])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotations[-1])
    plt.subplots_adjust(left=0.08, bottom=0.07, right=0.97, top=0.93, hspace=0.42)  # 调整页面边距、子图间距
    fig.savefig(price_by_district_box_image)
    plt.show()


if __name__ == "__main__":
    # 加载预处理后的csv数据, 并拓展缺失值
    filename = proc_file.format(city_abbr, task)
    df = pd.read_csv(filename, na_values=na_values)
    # print(df.info())
    # paint_wordcloud(df)
    # paint_basic_info_distrib(df)
    # paint_stats_by_district(df)
    # paint_price_area_distribution(df)
    # paint_unitprice_topk_communities(df)  # √
    # paint_price_by_district_box(df)  # √

