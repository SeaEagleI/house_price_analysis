import json
import numpy as np
from tqdm import tqdm
from city import update_city
from config import json_file
from ershoufang import city_id, city_abbr, update_total_houses, get_ershoufang_info

# params
main_task = "ershoufang"
sub_task = "complement"
ershoufang_json = json_file.format(city_abbr, main_task)
complement_json = json_file.format(city_abbr, sub_task)

# Scheduler: Params
Total = 88646
Sum_Bc = 88648
Sum_Proc_Len = 88648
Unit = 2954.9
Avg_ABS = 16.2
Workers = 30
Bc_Lens = {611100697: 2509, 18335711: 1923, 611100696: 1829, 611100360: 1688, 611100608: 1637, 18335745: 1570, 18335747: 1210, 1100007014: 1204, 611100412: 1134, 18335774: 1119, 611100404: 1076, 611100362: 996, 611100316: 956, 611100364: 937, 18335750: 912, 611100308: 910, 18335749: 890, 611100405: 890, 611100343: 875, 18335682: 867, 18335751: 861, 611100328: 817, 18335631: 761, 1100006766: 728, 611100346: 709, 18335714: 697, 18335706: 692, 611100531: 684, 18335729: 676, 611100610: 676, 18335694: 670, 611100711: 670, 611100712: 668, 18335703: 660, 18335689: 645, 611100365: 642, 611100611: 612, 18335778: 609, 18335676: 605, 18335702: 584, 611100397: 579, 611100329: 574, 18335699: 563, 611100366: 541, 18335715: 537, 611100315: 532, 611100800: 532, 18335728: 531, 18335696: 531, 18335710: 529, 18335701: 528, 611100368: 517, 18335685: 510, 18335727: 494, 611100323: 490, 611100797: 471, 611100309: 462, 18335780: 456, 18335737: 451, 1100006545: 443, 18335746: 439, 18335704: 433, 18335641: 428, 611100601: 428, 18335738: 425, 18335735: 424, 611100322: 424, 18335669: 421, 18335724: 421, 611100595: 420, 18335744: 408, 611100716: 408, 611100392: 404, 18335700: 400, 1100007016: 393, 18335670: 383, 18335713: 378, 1100007040: 376, 18335743: 375, 611100715: 370, 18335770: 362, 18335707: 360, 18335662: 345, 18335666: 341, 18335766: 339, 611100349: 339, 18335625: 337, 1100007028: 336, 1100006544: 331, 18335723: 326, 18335630: 326, 611100609: 323, 611100796: 320, 611100350: 309, 611100324: 308, 18335636: 306, 18335734: 304, 18335681: 304, 611100319: 303, 611100547: 302, 611100717: 300, 18335679: 294, 611100596: 294, 18335644: 293, 611100326: 291, 611100339: 290, 18335624: 289, 611100448: 288, 611100321: 287, 18335683: 287, 611100537: 285, 1100007017: 285, 18335680: 284, 611100612: 281, 18335654: 280, 611100334: 274, 18335687: 274, 18335629: 272, 18335739: 267, 611100710: 264, 611100801: 263, 611100345: 260, 18335718: 258, 611100332: 257, 18335633: 256, 18335655: 255, 18335730: 255, 611100352: 252, 611100356: 247, 611100344: 247, 1100007223: 246, 18335767: 242, 18335726: 241, 18335634: 240, 18335627: 239, 611100337: 238, 18335639: 237, 18335686: 235, 18335695: 224, 611100353: 223, 1100006835: 219, 611100333: 218, 611100325: 217, 611100358: 213, 18335709: 212, 18335754: 212, 611100395: 212, 611100536: 210, 611100341: 208, 18335674: 208, 18335692: 207, 18335693: 207, 18335667: 206, 18335628: 206, 18335653: 204, 611100357: 204, 611100310: 203, 18335678: 202, 611100351: 201, 18335779: 200, 18335741: 199, 611100614: 194, 611100446: 193, 18335691: 193, 18335623: 192, 611100355: 190, 611100400: 190, 18335640: 187, 18335684: 185, 18335768: 183, 1100004031: 183, 611100361: 183, 611100432: 181, 611100481: 181, 18335647: 180, 18335740: 180, 611100709: 180, 611100318: 179, 18335782: 176, 611100573: 175, 18335656: 174, 611100367: 174, 611100431: 172, 611100327: 169, 611100347: 169, 611100698: 166, 611100535: 166, 611100313: 153, 611100359: 152, 18335722: 152, 611100799: 150, 611100348: 144, 611100403: 143, 611100330: 142, 611100314: 140, 18335717: 139, 611100338: 138, 611100466: 138, 611100445: 137, 18335773: 135, 1100006546: 131, 611100718: 127, 1100006187: 126, 611100529: 123, 611100597: 118, 611100402: 113, 18335672: 109, 18335716: 108, 611100363: 105, 611100342: 103, 18335657: 102, 18335757: 101, 1100007144: 97, 18335675: 92, 18335671: 89, 18335658: 87, 18335761: 86, 18335762: 84, 611100396: 83, 613000370: 82, 18335758: 81, 611100331: 80, 611100447: 78, 611100320: 71, 18335665: 70, 611100354: 69, 611100699: 68, 18335661: 66, 1100007166: 63, 611100444: 58, 18335698: 56, 18335760: 54, 18335652: 52, 611100442: 51, 611100714: 50, 611100340: 42, 18335632: 42, 611100401: 40, 611100406: 39, 611100713: 35, 611100335: 25, 611100398: 23, 1100007019: 21, 18335673: 17, 611100443: 16, 1100005681: 15, 611100336: 14, 18335645: 12, 611100399: 3, 1100007035: 2, 1100007033: 1, 611100798: 0, 611100719: 0, 1100007039: 0, 1100007042: 0, 1100007038: 0, 1100007037: 0, 1100007043: 0, 1100007036: 0, 1100007021: 0, 1100007030: 0, 1100007029: 0, 1100007034: 0, 1100007044: 0, 1100007041: 0}
Proc_Lens = [2952, 2919, 2948, 2898, 2841, 2956, 2944, 2955, 2955, 2956, 2953, 2953, 2952, 2958, 2954, 2954, 2956, 2954, 2959, 2955, 2954, 2957, 2954, 2960, 2955, 2952, 2954, 2961, 2955, 3174]
Schedule_List = [[(611100697, '长阳'), (1100006545, '大兴新机场')],
                 [(18335711, '望京'), (611100362, '马坡')],
                 [(611100696, '良乡'), (18335774, '怀柔')],
                 [(611100360, '顺义城'), (18335747, '天通苑')],
                 [(611100608, '枣园'), (1100007014, '鼓楼街道')],
                 [(18335745, '回龙观'), (611100412, '北苑'), (611100352, '花乡')],
                 [(611100404, '顺义其它'), (611100316, '双井'), (18335750, '亦庄')],
                 [(611100364, '后沙峪'), (611100308, '北七家'), (18335749, '旧宫'), (611100333, '欢乐谷')],
                 [(611100405, '通州其它'), (611100343, '科技园区'), (18335682, '马家堡'), (611100609, '新宫')],
                 [(18335751, '西红门'), (611100328, '常营'), (18335631, '清河'), (611100368, '潘家园')],
                 [(1100006766, '高米店'), (611100346, '临河里'), (18335714, '双桥'), (18335706, '亚运村'), (611100718, '冯村')],
                 [(611100531, '九棵树(家乐福)'), (18335729, '朝青'), (611100610, '天宫院'), (18335694, '鲁谷'), (611100356, '马连洼')],
                 [(611100711, '阎村'), (611100712, '窦店'), (18335703, '武夷花园'), (18335689, '玉泉营'), (611100350, '宋家庄')],
                 [(611100365, '潞苑'), (611100611, '黄村中'), (18335778, '马驹桥'), (18335676, '方庄'), (611100323, '奥林匹克公园')],
                 [(18335702, '万达'), (611100397, '丰台其它'), (611100329, '大望路'), (18335699, '通州北苑'), (611100366, '北关'),
                  (611100402, '平谷其它')],
                 [(18335715, '百子湾'), (611100315, '亚运村小营'), (611100800, '东关'), (18335728, '石佛营'), (18335696, '苹果园'), (611100326, '东大桥')],
                 [(18335710, '酒仙桥'), (18335701, '果园'), (18335685, '青塔'), (18335727, '四惠'), (611100797, '鼓楼大街'), (18335735, 'CBD')],
                 [(611100309, '沙河'), (18335780, '东坝'), (18335737, '劲松'), (18335746, '西三旗'), (18335704, '安贞'), (18335641, '和平里'),
                  (611100537, '海淀北部新区')],
                 [(611100601, '马甸'), (18335738, '首都机场'), (611100322, '垡头'), (18335669, '广安门'), (18335724, '定福庄'),
                  (611100595, '亦庄开发区其它'), (18335744, '立水桥'), (18335645, '东单')],
                 [(611100716, '大峪'), (611100392, '昌平其它'), (18335700, '梨园'), (1100007016, '果园街道'), (18335670, '马连道'), (18335713, '豆各庄'),
                  (1100007040, '古北口镇'), (611100358, '四季青')],
                 [(18335743, '红庙'), (611100715, '城关'), (18335770, '中央别墅区'), (18335707, '芍药居'), (18335662, '崇文门'), (18335666, '广渠门'),
                  (18335766, '苏州桥'), (611100349, '刘家窑'), (611100529, '万寿路')],
                 [(18335625, '紫竹桥'), (1100007028, '溪翁庄镇'), (1100006544, '南中轴机场商务区'), (18335723, '管庄'), (18335630, '五棵松'),
                  (611100796, '西关环岛'), (611100324, '惠新西街'), (18335636, '五道口'), (18335734, '国展'), (1100007166, '杨镇')],
                 [(18335681, '大红门'), (611100319, '甜水园'), (611100547, '角门'), (611100717, '滨河西区'), (18335679, '六里桥'), (611100596, '北京南站'),
                  (18335644, '东直门'), (611100339, '六铺炕'), (18335624, '公主坟'), (1100007017, '密云镇')],
                 [(611100448, '朝阳门外'), (611100321, '西坝河'), (18335683, '卢沟桥'), (18335680, '菜户营'), (611100612, '黄村火车站'),
                  (18335654, '西直门'), (611100334, '陶然亭'), (18335687, '岳各庄'), (18335629, '万柳'), (18335739, '朝阳公园'), (611100698, '三里屯')],
                 [(611100710, '城子'), (611100801, '南邵'), (611100345, '和义'), (18335718, '华威桥'), (611100332, '成寿寺'), (18335633, '上地'),
                  (18335655, '月坛'), (18335730, '团结湖'), (611100344, '赵公口'), (1100007223, '上岸地铁'), (18335767, '皂君庙'), (611100359, '木樨地')],
                 [(18335726, '甘露园'), (18335634, '定慧寺'), (18335627, '学院路'), (611100337, '西罗园'), (18335639, '知春路'), (18335686, '太平桥'),
                  (18335695, '杨庄'), (611100353, '甘家口'), (1100006835, '大兴新机场洋房别墅区'), (611100325, '高碑店'), (18335709, '三元桥'),
                  (18335754, '小西天'), (611100395, '大兴其它'), (611100399, '怀柔其它')],
                 [(611100536, '玉桥'), (611100341, '蒲黄榆'), (18335674, '牛街'), (18335692, '八角'), (18335693, '古城'), (18335667, '永定门'),
                  (18335628, '世纪城'), (18335653, '新街口'), (611100357, '田村'), (611100310, '霍营'), (18335678, '洋桥'), (611100351, '草桥'),
                  (18335779, '工体'), (18335741, '十里堡'), (18335671, '白纸坊')],
                 [(611100614, '观音寺'), (611100446, '建国门外'), (18335691, '玉泉路'), (18335623, '中关村'), (611100355, '双榆树'),
                  (611100400, '门头沟其它'), (18335640, '军博'), (18335684, '木樨园'), (18335768, '牡丹园'), (1100004031, '瀛海'), (611100361, '李桥'),
                  (611100432, '右安门内'), (611100481, '健翔桥'), (18335647, '安定门'), (18335740, '太阳宫'), (611100535, '西北旺')],
                 [(611100709, '燕山'), (611100318, '南沙滩'), (18335782, '看丹桥'), (611100573, '七里庄'), (18335656, '阜成门'), (611100367, '乔庄'),
                  (611100431, '右安门外'), (611100327, '农展馆'), (611100347, '北大地'), (611100313, '小汤山'), (18335722, '燕莎'), (611100799, '南口'),
                  (611100348, '丽泽'), (611100403, '石景山其它'), (611100330, '北工大'), (611100314, '西二旗'), (18335717, '十里河'),
                  (611100338, '东花市'), (18335761, '白石桥')],
                 [(611100466, '安宁庄'), (611100445, '朝阳门内'), (18335773, '五里店'), (1100006546, '义和庄'), (1100006187, '亮马桥'),
                  (611100597, '天宁寺'), (18335672, '长椿街'), (18335716, '十八里店'), (611100363, '天竺'), (611100342, '金融街'), (18335657, '车公庄'),
                  (18335757, '二里庄'), (1100007144, '万源'), (18335675, '宣武门'), (18335658, '官园'), (18335762, '西山'), (611100396, '房山其它'),
                  (613000370, '朝阳其它'), (18335758, '魏公村'), (611100331, '左安门'), (611100447, '建国门内'), (611100320, '大山子'), (18335665, '天坛'),
                  (611100354, '圆明园'), (611100699, '颐和园'), (18335661, '西单'), (611100444, '东四'), (18335698, '老山'), (18335760, '厂洼'),
                  (18335652, '德胜门'), (611100442, '灯市口'), (611100714, '韩村河'), (611100340, '西四'), (18335632, '北太平庄'), (611100401, '密云其它'),
                  (611100406, '延庆其它'), (611100713, '琉璃河'), (611100335, '交道口'), (611100398, '海淀其它'), (1100007019, '十里堡镇'),
                  (18335673, '前门'), (611100443, '金宝街'), (1100005681, '天宫院南'), (611100336, '地安门'), (1100007035, '太师屯镇'),
                  (1100007033, '西田各庄镇'), (611100798, '百善镇'), (611100719, '石门营'), (1100007039, '北庄镇'), (1100007042, '不老屯镇'),
                  (1100007038, '大城子镇'), (1100007037, '东邵渠镇'), (1100007043, '冯家峪镇'), (1100007036, '高岭镇'), (1100007021, '河南寨镇'),
                  (1100007030, '巨各庄镇'), (1100007029, '穆家峪镇'), (1100007034, '石城镇'), (1100007044, '檀营'), (1100007041, '新城子镇')],
                 ]

# check & recover result
# brief_schedules = [[x[0] for x in sch] for sch in Schedule_List]
# Proc_Lens = [sum(Bc_Lens[bid] for bid in sch) for sch in brief_schedules]
# print(Proc_Lens)
# print(np.mean(np.abs(np.array(Proc_Lens) - Unit)))

# check proc 19
# sch_19 = Schedule_List[19]
# bc_lens_19 = {bid: Bc_Lens[bid] for bid, bname in sch_19}
# print(bc_lens_19)

# complement crawl for missed bc "1100007040"
# pid = 19
# city, district_dict, bizcircle_list = update_city(city_id, city_abbr)
# bizcircle_dict = {b.id: b for b in bizcircle_list}
# proc_bizcircle_list = [bizcircle_dict[1100007040]]
# proc_len = sum(update_total_houses(city_id, b.quan_pin) for b in tqdm(proc_bizcircle_list, desc="Update bc houses"))
# proc_house_dict = get_ershoufang_info(city_id, district_dict, proc_bizcircle_list, proc_len, pid)
# print("Len {} for complement: {}".format(len(proc_house_dict), [(b.id, b.name) for b in proc_bizcircle_list]))
# json.dump(proc_house_dict, open(complement_json, "w+", encoding="utf-8"), ensure_ascii=False, indent=4)
proc_house_dict = json.load(open(complement_json, encoding="utf-8"))
house_dict = json.load(open(ershoufang_json, encoding="utf-8"))
last_size = len(house_dict)
house_dict.update(proc_house_dict)
print(f"Len {last_size} -> {len(house_dict)}, {len(house_dict) - last_size} Added")
json.dump(house_dict, open(ershoufang_json, "w+", encoding="utf-8"), ensure_ascii=False, indent=4)