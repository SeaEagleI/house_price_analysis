import os, os.path as op

# Wordcloud text fields
text_fields = ["区域", "商圈", "小区", "交易权属", "产权所属", "供暖方式", "别墅类型",
               "建筑类型", "建筑结构", "户型结构", "房屋年限", "房屋户型", "房屋朝向", "房屋用途", "抵押信息",
               "梯户比例", "用水类型", "用电类型", "装修情况", "所在楼层",
               ]
cut_fields = ["榜单标题", "房源标题"]

# Resource Files
res_dir = "res"
mask_image = op.join(res_dir, "house_logo.jpg")

# Result Pictures
pic_dir = "pics"
ershoufang_pic_dir = op.join(pic_dir, "ershoufang")
wordcloud_image = op.join(ershoufang_pic_dir, "{}-{}.png")
price_by_district_image = op.join(ershoufang_pic_dir, "price_by_district_boxplot.png")
price_by_district_image = op.join(ershoufang_pic_dir, "price_by_district_boxplot.png")
price_by_district_image = op.join(ershoufang_pic_dir, "price_by_district_boxplot.png")
unitprice_topk_communities_image = op.join(ershoufang_pic_dir, "unitprice_top{}_communities_bar.png")
price_by_district_box_image = op.join(ershoufang_pic_dir, "price_by_district_box.png")



