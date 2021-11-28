# 每个图包括: 1)数据分组、数据运算和聚合; 2)绘图（bar/parallel_bar/box/pie/scatter）
import cv2
import jieba
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

from analysis.config import text_fields, cut_fields, colors, district_order, district_order_, \
    mask_image, wordcloud_image, price_by_district_distrib_image, unitprice_topk_communities_image, \
    stats_by_district_image, price_area_distrib_image, basic_info_distrib_image
from general_config import proc_file, city_abbr, na_values

task = "ershoufang"
max_total_houses = 100000
# 正常显示中文标签、负号
plt.rcParams["font.sans-serif"] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams["axes.unicode_minus"] = False


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
        wordcloud.to_file(wordcloud_image.format(bg_color))
        # plt.figure("二手房词云", figsize=(15, 15), dpi=150)  # 指定所绘图名称
        # plt.imshow(wordcloud)  # 以图片的形式显示词云
        # plt.axis("off")  # 关闭图像坐标系
        # plt.show()


# 房源基本信息分布 (pie, subplots=3x3)
def paint_basic_info_distrib(df):
    cols = ["房屋用途", "房屋户型", "装修情况", "配备电梯", "近地铁", "区域", "所在楼层", "楼层总数(层)", "建筑面积(㎡)"]
    k_list = [4] + [6] * 4 + [14, 6, None, None]
    level_list = [None] * 7 + [[0, 5, 10, 15, 20, 30, 50], [0, 50, 100, 150, 200, 300, 500, np.inf]]
    r, c = 5, 2
    # assert r * c == len(cols), "Error: cols length & matrix size not match"
    fig = plt.figure(figsize=(14, 35), dpi=150)
    for i, (col, k, levels) in enumerate(zip(cols, k_list, level_list)):
        title, unit = col.split("(")[0] + "分布", col.split("(")[-1].replace(")", "")
        raw_value_counts = df[col].value_counts()
        if i < 7:
            # 集中分布（主要是文本和布尔值, 前7个）
            pie_value_counts = raw_value_counts[:k]
            if len(raw_value_counts) > k:
                pie_value_counts["其他"] = raw_value_counts[k:].sum()
        else:
            # 高离散分布（数值, 后2个）
            labels = [f"{l}{unit}以上" if r == np.inf else f"{l}-{r}{unit}" for l, r in zip(levels[:-1], levels[1:])]
            pie_value_counts = pd.cut(df[col], levels, labels=labels).value_counts()
        ax = fig.add_subplot(r * 100 + c * 10 + i + 1)
        ax.set_title(title, y=0.96, fontsize=25)
        pie_value_counts.name = ""
        # print(col, '\n', pie_value_counts)
        pie_value_counts.plot(kind="pie", colormap="rainbow", autopct="%3.1f%%", fontsize=12)
    plt.subplots_adjust(left=0, bottom=0, right=0.99, top=0.99, wspace=0.05, hspace=0.05)  # 调整页面边距、子图间距
    fig.savefig(basic_info_distrib_image)
    plt.show()


# 各区域的房源数量、平均单价、平均建筑面积对比 (parallel_bar, par=3)
def paint_stats_by_district(df, bar_width=0.3):
    # 房源数量
    stats_by_district = df[["单价(元/㎡)", "建筑面积(㎡)"]].groupby(df["区域"]).mean().sort_values("单价(元/㎡)", ascending=False)
    stats_by_district["房源总数"] = df["houseCode"].groupby(df["区域"]).count()
    # 主要参数
    xtick_labels = district_order_
    x, bars = np.arange(len(xtick_labels)), []  # 柱状图在横坐标上的位置
    y0_label, y1_label, y2_label = "区域房源总数(套)", "平均单价(元/㎡)", "平均建筑面积(㎡)"
    scale = 5
    # 绘图
    fig = plt.figure(figsize=(20, 10), dpi=150)
    ax1 = fig.add_subplot(111)
    ax1.set_title("北京各区域二手房对比", y=1.03, fontsize=30)
    bars.append(ax1.bar(x - bar_width, stats_by_district["房源总数"] * scale, bar_width, color='b', label=y0_label))
    bars.append(ax1.bar(x, stats_by_district["单价(元/㎡)"], bar_width, color='r', label=y1_label))
    ax1.set_ylabel(y1_label, fontsize=22)
    ax1.set_yticks(np.arange(5 + 1) * 25000)
    # 显示x轴标签,即tick_label, 并调整位置使其落在两个直方图正中间
    ax1.set_xticks(x)
    ax1.set_xticklabels(xtick_labels, fontsize=15)
    # 第一Y轴标签、刻度颜色设置
    y1_color = bars[1][0].get_facecolor()
    ax1.yaxis.label.set_color(y1_color)
    ax1.tick_params(axis='y', colors=y1_color, labelsize=13)
    # 双Y轴设置
    ax2 = ax1.twinx()
    bars.append(ax2.bar(x + bar_width, stats_by_district["建筑面积(㎡)"], bar_width, color='g', label=y2_label))
    ax2.set_ylabel(y2_label, fontsize=22)
    ax2.set_yticks(np.arange(10 + 1) * 25)
    # 第二Y轴标签、刻度颜色设置
    y2_color = bars[-1][0].get_facecolor()
    ax2.yaxis.label.set_color(y2_color)
    ax2.tick_params(axis='y', colors=y2_color, labelsize=13)
    # 加数据标签
    for ax, bar, s in zip([ax1, ax1, ax2], bars, [scale, 1, 1]):
        for b in bar:
            ax.text(b.get_x() + bar_width / 2, b.get_height(), str(int(b.get_height() / s)), ha="center", va="bottom")
    plt.legend(handles=bars, fontsize=15)  # 显示图例，即label
    plt.subplots_adjust(left=0.09, bottom=0.15, right=0.92, top=0.90)  # 调整页面边距、子图间距
    # plt.grid("on")
    fig.savefig(stats_by_district_image)
    plt.show()


# 北京二手房单价与建筑面积区位分布 (scatter, cate=17)
def paint_price_area_distrib(df):
    fig = plt.figure(figsize=(25, 15), dpi=150)
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房单价与建筑面积散点图", y=1.02, fontsize=35)
    district_groups = dict(list(df[df["房屋用途"].apply(lambda x: x not in ["商业办公类", "车库"])].groupby("区域")))
    for d, c in zip(district_order, colors):
        district_groups[d].plot.scatter(x="建筑面积(㎡)", y="单价(元/㎡)", s=8, c=c, label=d, grid=True, fontsize=12,
                                        ax=ax, xticks=[0, 50, 100, 150, 200, 250, 300, 400, 500],
                                        xlim=[0, 500], ylim=[0, 180000])
    ax.set_xlabel("建筑面积(㎡)", fontsize=27)
    ax.set_ylabel("单价(元/㎡)", fontsize=27)
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    plt.legend(markerscale=8, fontsize=24)
    plt.subplots_adjust(left=0.06, bottom=0.05, right=0.98, top=0.93)  # 调整页面边距、子图间距
    fig.savefig(price_area_distrib_image)
    plt.show()


# 北京二手房均价最高小区TopK (parallel_bar, par=2)
def paint_unitprice_topk_communities(df, k=10, bar_width=0.4, rotation=30):
    unitprice_top_communities = df.groupby(["区域", "小区"]).mean().sort_values(["小区均价(元/㎡)"], ascending=False)[
                                    ["小区均价(元/㎡)", "建筑面积(㎡)"]][:k]
    # 主要参数
    xtick_labels = ["\n".join(indices) for indices in unitprice_top_communities.index]
    x, bars = np.arange(len(xtick_labels)), []  # 柱状图在横坐标上的位置
    y1_label, y2_label = "小区均价(元/㎡)", "平均建筑面积(㎡)"
    # 绘图
    fig = plt.figure(figsize=(14, 8), dpi=150)
    ax1 = fig.add_subplot(111)
    ax1.set_title(f"北京二手房单价Top{k}小区", y=1.03, fontsize=30)
    bars.append(
        ax1.bar(x - bar_width / 2, unitprice_top_communities["小区均价(元/㎡)"], bar_width, color='r', label=y1_label))
    ax1.set_ylabel(y1_label, fontsize=22)
    ax1.set_yticks(np.arange(9 + 1) * 25000)
    # 显示x轴标签,即tick_label, 并调整位置使其落在两个直方图正中间
    ax1.set_xticks(x)
    ax1.set_xticklabels(xtick_labels, rotation=rotation, fontsize=15)
    # 第一Y轴标签、刻度颜色设置
    # ax1.yaxis.label.set_color(bar1[0].get_facecolor())
    ax1.tick_params(axis='y', labelsize=13)
    # 双Y轴设置
    ax2 = ax1.twinx()
    bars.append(ax2.bar(x + bar_width / 2, unitprice_top_communities["建筑面积(㎡)"], bar_width, color='g', label=y2_label))
    ax2.set_ylabel(y2_label, fontsize=22)
    ax2.set_yticks(np.arange(9 + 1) * 50)
    # 第二Y轴标签、刻度颜色设置
    ax2.yaxis.label.set_color(bars[1][0].get_facecolor())
    ax2.tick_params(axis='y', colors=bars[1][0].get_facecolor(), labelsize=13)
    # 加数据标签
    for ax, bar in zip([ax1, ax2], bars):
        for b in bar:
            ax.text(b.get_x() + bar_width / 2, b.get_height(), str(int(b.get_height())), ha="center", va="bottom")
    plt.legend(handles=bars, fontsize=15)  # 显示图例，即label
    plt.subplots_adjust(left=0.09, bottom=0.15, right=0.92, top=0.90)  # 调整页面边距、子图间距
    # plt.grid("on")
    fig.savefig(unitprice_topk_communities_image.format(k))
    plt.show()


# 北京各区域二手房价格箱线图 (box, subplots=2x1)
def paint_price_by_district_distrib(df, rotation=60):
    # 二手房单价箱线图
    unitprice_groups_by_district = dict(sorted(list(df["单价(元/㎡)"].groupby(df["区域"])),
                                               key=lambda x: x[1].mean(), reverse=True))
    box_data = pd.DataFrame(list(range(max_total_houses)), columns=["tmp"])
    for name, group in unitprice_groups_by_district.items():
        box_data[name] = group
    del box_data["tmp"]
    # 绘图
    fig = plt.figure(figsize=(20, 20), dpi=150)
    ax = fig.add_subplot(211)
    ax.set_title("北京各区域二手房单价箱线图", y=1.05, fontsize=45)
    ax.set_ylabel("单价(元/㎡)", fontsize=22)
    box_data.plot(kind="box", fontsize=20, sym="r+", grid=True, ax=ax,
                  yticks=[10000, 20000, 30000, 40000, 50000, 100000, 150000, 180000], ylim=[0, 180000])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
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
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
    plt.subplots_adjust(left=0.08, bottom=0.07, right=0.97, top=0.93, hspace=0.42)  # 调整页面边距、子图间距
    fig.savefig(price_by_district_distrib_image)
    plt.show()


if __name__ == "__main__":
    # 加载预处理后的csv数据, 并拓展缺失值
    filename = proc_file.format(city_abbr, task)
    df = pd.read_csv(filename, na_values=na_values)
    # print(df.info())
    paint_wordcloud(df)  # √
    paint_basic_info_distrib(df)  # √
    paint_stats_by_district(df)  # √
    paint_price_area_distrib(df)  # √
    paint_unitprice_topk_communities(df)  # √
    paint_price_by_district_distrib(df)  # √
