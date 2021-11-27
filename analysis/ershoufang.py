import cv2
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from general_config import proc_file, city_abbr, na_values
from analysis.config import text_fields, cut_fields, mask_image, wordcloud_image

task = "ershoufang"
max_total_houses = 100000
# 用来正常显示中文标签
plt.rcParams["font.sans-serif"] = ["SimHei"]
# 用来正常显示负号
plt.rcParams["axes.unicode_minus"] = False


# 每个图包括: 1)数据分组、数据运算和聚合; 2)绘图（bar/parallel_bar/box/pie/scatter）
def paint(df):
    """房源价格信息"""
    """北京各区域二手房平均单价"""  # parallel bar
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
    groups_area_jzmj = df["建筑面积(㎡)"].groupby(df["区域"])
    mean_jzmj = groups_area_jzmj.mean()
    mean_jzmj.index.name = ""
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("建筑面积(㎡)", fontsize=14)
    ax.set_title("北京各区域二手房平均建筑面积", fontsize=18)
    mean_jzmj.plot(kind="bar", fontsize=12)
    plt.show()
    # """北京各区域平均单价和平均建筑面积"""
    # groups_unitprice_area = df["单价(元/㎡)"].groupby(df["区域"])
    # mean_unitprice_by_district = groups_unitprice_area.mean()
    # mean_unitprice_by_district.index.name = ""
    # groups_area_jzmj = df["建筑面积(㎡)"].groupby(df["区域"])
    # mean_jzmj = groups_area_jzmj.mean()
    # mean_jzmj.index.name = ""
    # fig = plt.figure()
    # ax1 = fig.add_subplot(2, 1, 1)
    # ax1.set_ylabel("单价(元/平米)", fontsize=14)
    # ax1.set_title("北京各区域二手房平均单价", fontsize=18)
    # ax2 = fig.add_subplot(2, 1, 2)
    # ax2.set_ylabel("建筑面积(㎡)", fontsize=14)
    # ax2.set_title("北京各区域二手房平均建筑面积", fontsize=18)
    # plt.subplots_adjust(hspace=0.4)
    # mean_unitprice_by_district.plot(kind="bar", ax=ax1, fontsize=12)
    # mean_jzmj.plot(kind="bar", ax=ax2, fontsize=12)
    # plt.show()

    """北京各区域二手房单价箱线图"""  # box
    unitprice_groups_by_district = df["单价(元/㎡)"].groupby(df["区域"])
    box_data = pd.DataFrame(list(range(max_total_houses)), columns=["tmp"])
    for name, group in unitprice_groups_by_district:
        box_data[name] = group
    del box_data["tmp"]
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("总价(万元)", fontsize=14)
    ax.set_title("北京各区域二手房单价箱线图", fontsize=18)
    box_data.plot(kind="box", fontsize=12, sym="r+", grid=True, ax=ax, yticks=[20000, 30000, 40000, 50000, 100000])
    """北京各区域二手房总价箱线图"""
    box_total_area = df["总价(万元)"].groupby(df["区域"])
    box_data = pd.DataFrame(list(range(max_total_houses)), columns=["tmp"])
    for name, group in box_total_area:
        box_data[name] = group
    del box_data["tmp"]
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("总价(万元)", fontsize=14)
    ax.set_title("北京各区域二手房总价箱线图", fontsize=18)
    box_data.plot(kind="box", fontsize=12, sym="r+", grid=True, ax=ax, yticks=[0, 500, 1000, 2000, 3000, 5000, 10000])

    """北京二手房小区均价最高Top20"""  # bar
    avgprice

    unitprice_top = df.sort_values(by="小区均价(元/㎡)", ascending=False)[:20]
    # unitprice_top = unitprice_top.sort_values(by="单价(元/㎡)")
    unitprice_top.set_index(unitprice_top["小区"], inplace=True)
    unitprice_top.index.name = ""
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("单价(元/平米)", fontsize=14)
    ax.set_title("北京二手房单价最高Top20", fontsize=18)
    unitprice_top["单价(元/㎡)"].plot(kind="bar", fontsize=12)
    plt.show()

    """北京二手房单价与建筑面积散点图"""  # scatter
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房单价与建筑面积散点图", fontsize=18)
    df.plot(x="建筑面积(㎡)", y="单价(元/㎡)", kind="scatter", grid=True, fontsize=12, ax=ax, alpha=0.4,
            xticks=[0, 50, 100, 150, 200, 250, 300, 400, 500, 600, 700], xlim=[0, 800])
    ax.set_xlabel("建筑面积(㎡)", fontsize=14)
    ax.set_ylabel("单价(元/平米)", fontsize=14)
    plt.show()

    """房源基本信息"""  # pie
    # 房屋用途分布

    # 房屋户型分布
    count_fwhx = df["房屋户型"].value_counts()[:10]
    count_other_fwhx = pd.Series({"其他": df["房屋户型"].value_counts()[10:].count()})
    count_fwhx = count_fwhx.append(count_other_fwhx)
    count_fwhx.index.name = ""
    count_fwhx.name = ""
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房房屋户型占比情况", fontsize=18)
    count_fwhx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    plt.show()
    # 装修情况分布
    count_zxqk = df["装修情况"].value_counts()
    count_zxqk.name = ""
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房装修占比情况", fontsize=18)
    count_zxqk.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    plt.show()
    # 建筑类型分布
    count_jzlx = df["建筑类型"].value_counts()
    count_jzlx.name = ""
    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111)
    ax.set_title("北京二手房建筑类型占比情况", fontsize=18)
    count_jzlx.plot(kind="pie", cmap=plt.cm.rainbow, autopct="%3.1f%%", fontsize=12)
    plt.show()
    # 房屋朝向分布
    count_fwcx = df["房屋朝向"].value_counts()[:15]
    count_other_fwcx = pd.Series({"其他": df["房屋朝向"].value_counts()[15:].count()})
    count_fwcx = count_fwcx.append(count_other_fwcx)
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_title("房源朝向分布情况", fontsize=18)
    count_fwcx.plot(kind="bar", fontsize=12)
    plt.show()
    # 建筑面积分布(区间)
    area_level = [0, 50, 100, 150, 200, 250, 300, 500, 100000]
    label_level = ["小于50", "50-100", "100-150", "150-200", "200-250", "250-300", "300-500", "大于500"]
    jzmj_cut = pd.cut(df["建筑面积(㎡)"], area_level, labels=label_level)
    jzmj_result = jzmj_cut.value_counts()
    print(jzmj_result)
    # jzmj_result = jzmj_result.sort_values()
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111)
    ax.set_ylabel("建筑面积(㎡)", fontsize=14)
    ax.set_title("北京二手房建筑面积分布区间", fontsize=18)
    jzmj_result.plot(kind="pie", fontsize=12)
    plt.show()


# 北京二手房词云
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


if __name__ == "__main__":
    # 加载预处理后的csv数据, 并拓展缺失值
    filename = proc_file.format(city_abbr, task)
    df = pd.read_csv(filename, na_values=na_values)
    print(df.info())
    paint(df)
