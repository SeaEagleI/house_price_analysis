import os, os.path as op

# City
city_id = 110000
city_abbr = "bj"

# Task
main_tasks = ["ershoufang", "zufang"]    # including json/csv/preprocess files
sub_tasks = ["city_info", "complement"]  # including json file only

# Files
data_dir = "../data"
json_file = op.join(data_dir, "{}_{}.json")               # 1 for city_abbr, 2 for task from main_tasks & sub_tasks
csv_file = op.join(data_dir, "{}_{}.csv")
proc_file = op.join(data_dir, "{}_{}_preprocessed.csv")
# Create dir
if not op.exists(data_dir):
    os.makedirs(data_dir)
