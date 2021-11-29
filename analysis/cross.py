# 每个图包括: 1)数据分组、数据运算和聚合; 2)绘图（bar/parallel_bar/box/pie/scatter）
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.config import district_order, district_order_, house_counts_by_district_image, stats_by_bizcircle_image
from general_config import proc_file, city_abbr, na_values

cross_tasks = ["ershoufang", "zufang", "newhouse"]
encodings = ["utf-8", "gbk", "gbk"]
# 正常显示中文标签、负号
plt.rcParams["font.sans-serif"] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams["axes.unicode_minus"] = False


# Preprocess field "converged_rooms.area_range" values in newhouse_df to standard "area" format
def pro(x):
    x = str(x).replace("㎡", "")
    if "-" in x:
        x = np.array([float(i) for i in x.split("-")]).mean()
    return float(x)


# 各区域的二手房、租房、新房三种房源数量对比 (parallel_bar, par=3)
def paint_house_counts_by_district(df_list, bar_width=0.3):
    # 房源数量
    type_dict = {
        "二手房房源数(套)": ["houseCode", "区域"],
        "租房房源数(套)": ["house_code", "district_name"],
        "新房房源数(套)": ["id", "district_name"],
    }
    houses_by_district = pd.DataFrame(index=district_order)
    for df, (col, (count_col, group_col)) in zip(df_list, type_dict.items()):
        houses_by_district[col] = df[group_col].value_counts()
    houses_by_district.fillna(0, inplace=True)
    houses_by_district["desc"] = pd.Series(district_order_, index=district_order)
    houses_by_district.sort_values("二手房房源数(套)", ascending=False, inplace=True)
    print(houses_by_district)
    # 主要参数
    xtick_labels = houses_by_district["desc"]
    x, bars = np.arange(len(xtick_labels)), []  # 柱状图在横坐标上的位置
    # 绘图
    fig = plt.figure(figsize=(18, 10), dpi=150)
    ax = fig.add_subplot(111)
    ax.set_title("北京各区域三种房源数量对比", y=1.02, fontsize=30)
    for x_, c, label in zip([x - bar_width, x, x + bar_width], ["r", "b", "g"], type_dict):
        bar = ax.bar(x_, houses_by_district[label], bar_width, color=c, label=label)
        for b in bar:
            ax.text(b.get_x() + bar_width / 2, b.get_height(), str(int(b.get_height())), ha="center", va="bottom",
                    fontsize=13)
        bars.append(bar)
    # 设置x轴、公共y轴标签位置、内容
    ax.set_ylabel("房源数(套)", fontsize=22)
    ax.set_yticks(np.arange(11 + 1) * 2000)
    ax.set_ylim([0, 22000])
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels, fontsize=19)
    # 加数据标签
    plt.legend(handles=bars, fontsize=20)  # 显示图例，即label
    plt.subplots_adjust(left=0.06, bottom=0.07, right=0.99, top=0.92)  # 调整页面边距、子图间距
    # plt.grid("on")
    fig.savefig(house_counts_by_district_image)
    plt.show()


# 各商圈的新房与临近二手房价格、面积对比（parallel_line, par=4）
def compare_stats_by_bizcircle(esf_df, nh_df, line_width=2, rotation=90):
    types, labels = ["二手房", "新房"], ["平均单价(元/㎡)", "平均建筑面积(㎡)"]
    cols = [f"{type}{label}" for type in types for label in labels]
    colors = ["r", "lime", "m", "g"]
    nh_df = nh_df[nh_df["house_type"] != "写字楼"]
    nh_df["area"] = nh_df["converged_rooms.area_range"].apply(pro)
    cmp_df = pd.DataFrame(index=nh_df[["district_name", "bizcircle_name"]].value_counts().index)
    cmp_df[cols[:2]] = esf_df.groupby(["区域", "商圈"])[["单价(元/㎡)", "建筑面积(㎡)"]].mean()
    cmp_df[cols[2:]] = nh_df.groupby(["district_name", "bizcircle_name"])[["average_price", "area"]].mean()
    cmp_df = cmp_df[cmp_df[cols[0]].notna()][cmp_df[cols[-1]].notna()]
    # cmp_df["unitprice_ratio"] = cmp_df[cols[2]]/cmp_df[cols[0]]
    # cmp_df["area_ratio"] = cmp_df["新房平均建筑面积(㎡)"]/cmp_df["二手房平均建筑面积(㎡)"]
    cmp_df.sort_values(cols[2], ascending=False, inplace=True)
    # 主要参数
    xtick_labels = [f"{b}-{d}" for d, b in cmp_df.index]
    x, lines = np.arange(len(xtick_labels)), []  # 柱状图在横坐标上的位置
    y1_label, y2_label = labels
    y1_color, y2_color = colors[0], colors[-1]
    # 绘图
    fig = plt.figure(figsize=(20, 10), dpi=150)
    ax1 = fig.add_subplot(111)
    ax1.set_title(f"北京各商圈二手房、新房对比", y=1.03, fontsize=30)
    for label, color in zip(cols[0::2], colors[0::2]):
        lines.append(ax1.plot(x, cmp_df[label], "-", linewidth=line_width, color=color, label=label)[0])
    ax1.set_ylabel(y1_label, fontsize=22)
    ax1.set_yticks(np.arange(7 + 1) * 20000)
    # 显示x轴标签,即tick_label, 并调整位置使其落在两个直方图正中间
    ax1.set_xticks(x)
    ax1.set_xticklabels(xtick_labels, rotation=rotation, fontsize=15)
    # 第一Y轴标签、刻度颜色设置
    ax1.yaxis.label.set_color(y1_color)
    ax1.tick_params(axis='y', colors=y1_color, labelsize=13)
    # 双Y轴设置
    ax2 = ax1.twinx()
    for label, color in zip(cols[1::2], colors[1::2]):
        lines.append(ax2.plot(xtick_labels, cmp_df[label], "-", linewidth=line_width, color=color, label=label)[0])
    ax2.set_ylabel(y2_label, fontsize=22)
    ax2.set_yticks(np.arange(10 + 1) * 100)
    # ax2.set_ylim([0, 10 * 100])
    # 第二Y轴标签、刻度颜色设置
    ax2.yaxis.label.set_color(y2_color)
    ax2.tick_params(axis='y', colors=y2_color, labelsize=13)
    plt.legend(handles=lines, fontsize=15)  # 显示图例，即label
    plt.subplots_adjust(left=0.05, bottom=0.28, right=0.96, top=0.92)  # 调整页面边距、子图间距
    plt.grid("on")
    fig.savefig(stats_by_bizcircle_image)
    plt.show()


if __name__ == "__main__":
    # 加载预处理后的csv数据, 并拓展缺失值
    task_df_data = []
    for task, enc in zip(cross_tasks, encodings):
        task_df_data.append(pd.read_csv(open(proc_file.format(city_abbr, task), encoding=enc), na_values=na_values))
        # print(df.info())
    paint_house_counts_by_district(task_df_data)  # √
    compare_stats_by_bizcircle(task_df_data[0], task_df_data[-1])  # √
