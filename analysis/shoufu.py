import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from analysis.calc_shoufu import get_max_loan
from analysis.config import district_order_, stats_by_district_image, district_order, shoufu_by_district_image, \
    shoufu_distrib_image
from general_config import proc_file, city_abbr, na_values, json_file

task = "ershoufang"
sub_task = "xiaoqu_pos"
max_total_houses = 100000
target_district = "海淀"
# 正常显示中文标签、负号
plt.rcParams["font.sans-serif"] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams["axes.unicode_minus"] = False


# 各区域的首付、修正首付、总价对比 (parallel_bar, par=3)
def paint_shoufu_by_district(df, return_year=30, bar_width=0.3):
    max_loan = int(get_max_loan(return_year))
    # 房源数量
    cols = ["平均税费合计(万元)", "平均最低净首付(万元)", "修正最低净首付(万元)", "平均总价(万元)"]
    stats_by_district = pd.DataFrame({"desc": district_order_}, index=district_order)
    stats_by_district[cols[:2] + cols[3:]] = df[["税费合计(万元)", "净首付(万元)", "总价(万元)"]].groupby(df["区域"]).mean()
    stats_by_district[cols[2]] = list(
        map(lambda x: max(x[0], x[1] - max_loan), zip(stats_by_district[cols[1]], stats_by_district[cols[3]])))
    stats_by_district.fillna(0, inplace=True)
    stats_by_district["total_shoufu"] = list(
        map(lambda x: x[0] + x[1], zip(stats_by_district[cols[0]], stats_by_district[cols[1]])))
    stats_by_district.sort_values("total_shoufu", ascending=False, inplace=True)
    # 主要参数
    xtick_labels = stats_by_district["desc"]
    x, top_bars, bot_bars = np.arange(len(xtick_labels)), [], []  # 柱状图在横坐标上的位置
    # 绘图
    fig = plt.figure(figsize=(18, 10), dpi=150)
    ax = fig.add_subplot(111)
    ax.set_title("北京各区域的首付、修正首付、总价对比", y=1.03, fontsize=30)
    for x_, c, col in zip([x - bar_width, x, x + bar_width], ["b", "g", "r"], cols[1:]):
        bot_bar = ax.bar(x_, stats_by_district[col], bar_width, color=c, label=col)
        top_bar = ax.bar(x_, stats_by_district[cols[0]], bar_width, bottom=stats_by_district[col], color="orange",
                         label=cols[0])
        # 加数据标签
        for bot_b, top_b in zip(bot_bar, top_bar):
            bot_height, top_height = bot_b.get_height(), bot_b.get_height() + top_b.get_height()
            ax.text(bot_b.get_x() + bar_width / 2, bot_height, str(int(bot_height)), ha="center", va="bottom",
                    fontsize=13)
            ax.text(top_b.get_x() + bar_width / 2, top_height, str(int(top_height)), ha="center", va="bottom",
                    fontsize=13)
        bot_bars.append(bot_bar)
        top_bars.append(top_bar)
    ax.set_ylabel("价格(万元)", fontsize=22)
    ax.set_yticks(np.arange(10 + 1) * 100)
    ax.set_ylim([0, 10 * 100])
    # 设置x轴、y轴标签及位置
    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels, fontsize=18)
    ax.tick_params(axis='y', labelsize=13)
    plt.legend(handles=[top_bars[0]] + bot_bars, fontsize=18)  # 显示图例，即label
    plt.subplots_adjust(left=0.05, bottom=0.07, right=0.99, top=0.91)  # 调整页面边距、子图间距
    # plt.grid("on")
    fig.savefig(shoufu_by_district_image)
    plt.show()


# 已知$max_loan=496, 不同首付可以分别买$target_district哪些地段的房子?
# 条件: 1) min_pure_shoufu = max($total_price - $max_loan, $pure_shoufu) [即修正后的最低净首付]
#      2) min_total_shoufu = $total_tax + min_pure_shoufu               [即修正后的最低首付总计]
# "$var"表示var变量的值已获得, 而未加"$"的变量值需要计算
# 本函数对min_total_shoufu的可变化范围作出统计(目标为海淀区50~100平米房源)
def paint_affordable_houses(df, return_year=30):
    max_loan = int(get_max_loan(return_year))
    col, range_col, unit = "min_total_shoufu", "shoufu_range", "万元"
    min_area, max_area = 50, 100
    df = df[df["区域"] == target_district]
    df = df[df["建筑面积(㎡)"].apply(lambda x: 50 <= x <= 100)]
    df[col] = list(map(lambda x: x[0] + max(x[1] - max_loan, x[2]), zip(df["税费合计(万元)"], df["总价(万元)"], df["净首付(万元)"])))
    levels = [0, 200, 300, 500, 750, np.inf]
    labels = [f"{l}{unit}以上" if r == np.inf else f"{l}-{r}{unit}" for l, r in zip(levels[:-1], levels[1:])]
    df[range_col] = pd.cut(df[col], levels, labels=labels)
    pie_value_counts = df[range_col].value_counts()
    pie_value_counts.name = ""
    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(111)
    ax.set_title(f"{target_district}区{min_area}-{max_area}㎡房源最低首付分布_年还{return_year}万", y=0.98, fontsize=25)
    pie_value_counts.plot(kind="pie", colormap="rainbow", autopct="%3.1f%%", fontsize=16)
    plt.subplots_adjust(left=0, bottom=0, right=0.98, top=0.92)  # 调整页面边距、子图间距
    fig.savefig(shoufu_distrib_image.format(target_district, min_area, max_area, return_year))
    plt.show()
    # 地理绘图: 没看出什么有用信息 (放弃)
    # for idx, (shoufu_label, data) in enumerate(df.groupby(range_col)):
    #     print(idx+1, shoufu_label, data.shape[0])
    #     str_head = "var heatmapData = ["
    #     for name, count in data["小区"].value_counts().items():
    #         lng, lat = xiaoqu_pos[name]
    #         str_head += '{' + f'"lng":{lng}, "lat":{lat}, "count":{count}' + '},'
    #     result = str_head[:-1] + "]"
    #     with open("pics/{}.js".format(idx + 1), 'w') as f:
    #         f.write(result)


if __name__ == "__main__":
    # 加载预处理后的csv数据, 并拓展缺失值
    filename = proc_file.format(city_abbr, task)
    df = pd.read_csv(filename, na_values=na_values)
    xiaoqu_pos = json.load(open(json_file.format(city_abbr, sub_task), encoding="utf-8"))
    # print(df.info())
    # paint_shoufu_by_district(df)
    paint_affordable_houses(df, return_year=30)
    paint_affordable_houses(df, return_year=20)
    paint_affordable_houses(df, return_year=10)
