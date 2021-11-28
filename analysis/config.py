import os, os.path as op

# Wordcloud text fields
text_fields = ["区域", "商圈", "小区", "交易权属", "产权所属", "供暖方式", "别墅类型",
               "建筑类型", "建筑结构", "户型结构", "房屋年限", "房屋户型", "房屋朝向", "房屋用途", "抵押信息",
               "梯户比例", "用水类型", "用电类型", "装修情况", "所在楼层",
               ]
cut_fields = ["榜单标题", "房源标题"]

# Districts
district_order = ['西城', '东城', '海淀', '朝阳', '丰台', '石景山', '亦庄开发区', '昌平',
                  '通州', '大兴', '顺义', '门头沟', '怀柔', '房山', '平谷', '密云', '延庆']
district_order_ = ['西城', '东城', '海淀', '朝阳', '丰台', '石景山', '亦庄\n开发区', '昌平',
                  '通州', '大兴', '顺义', '门头沟', '怀柔', '房山', '平谷', '密云', '延庆']
colors = ["red", "green", "blue", "yellow", "purple", "black", "pink", "orange",
          "cyan", "lime", "darkred", "firebrick", "olive", "crimson", "grey", "goldenrod", "m"]

# Resource Files
res_dir = "res"
mask_image = op.join(res_dir, "house_logo.jpg")

# Result Pictures
pic_dir = "pics"
ershoufang_pic_dir = op.join(pic_dir, "ershoufang")
wordcloud_image = op.join(ershoufang_pic_dir, "wordcloud-{}.png")
basic_info_distrib_image = op.join(ershoufang_pic_dir, "basic_info_distrib_pie.png")
stats_by_district_image = op.join(ershoufang_pic_dir, "stats_by_district_bar.png")
price_area_distrib_image = op.join(ershoufang_pic_dir, "price_area_distrib_scatter.png")
unitprice_topk_communities_image = op.join(ershoufang_pic_dir, "unitprice_top{}_communities_bar.png")
price_by_district_distrib_image = op.join(ershoufang_pic_dir, "price_by_district_box.png")
