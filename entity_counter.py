"""
实体计数
@author: zhang shilong
@date: 2022/04/05
"""
input_path = "litcovid.pubtator.pmid.txt"
count = {}

with open(input_path, "r", encoding="utf8") as file:

    for line in file.readlines():
        if "|a|" in line or "|t|" in line or not line.strip():
            continue
        contents = line.strip().split("\t")
        key = contents[3].lower()
        if key not in count.keys():
            count[key] = {"count": 1, "type": contents[4], "id": contents[5]}
        else:
            count[key]["count"] += 1

sorted_count = sorted(count.items(), key=lambda x: x[1]['count'])
# for k, v in sorted_count:
#     if v["type"] == "Mutation":
#         print(k, v)
print(sorted_count)
