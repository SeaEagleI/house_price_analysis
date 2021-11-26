from genJsFile import genJsFile, genJsFile2


def genCountMap(data_src, col, basic_map, target_name):
    target_data = target_name + ".js"
    target_map = "pic/" + target_name + ".html"
    genJsFile(data_src, col, target_data)
    with open(basic_map, "r", encoding="utf-8") as f:
        fcontent = f.read()
        fcontent = fcontent.replace("basic_map_data", target_name)
        with open(target_map, "w", encoding="utf-8") as f2:
            f2.write(fcontent)

def genPriceMap(data_src, basic_map, target_name):
    target_data = target_name + ".js"
    target_map = "pic/" + target_name + ".html"
    genJsFile2(data_src, target_data)
    with open(basic_map, "r", encoding="utf-8") as f:
        fcontent = f.read()
        fcontent = fcontent.replace("basic_map_data", target_name)
        with open(target_map, "w", encoding="utf-8") as f2:
            f2.write(fcontent)


if __name__ == "__main__":
    # genCountMap("../data/bj_ershoufang_preprocessed.csv", "小区", "data/basic_map.html", "HeatMap_count")
    # genPriceMap("../data/bj_ershoufang_preprocessed.csv", "data/basic_map.html", "HeatMap_price")
