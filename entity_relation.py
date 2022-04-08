"""
共句分析
@author: zhang shilong
@date: 2022/04/05
"""
input_path = "litcovid.pubtator.pmid.txt"
relation = {}

with open(input_path, "r", encoding="utf8") as file:

    for line in file.readlines():
        line = line.strip()
        if not line:
            continue
        if "|t|" in line:
            title = line.split("|")[2]
            continue
        if "|a|" in line:
            para = line.split("|")[2]
            sentences = para.split(". ")
            sentences.insert(0, title + "\n")

            cur_index = 0
            cur_start = 0
            cur_end = len(sentences[0]) - 1
            tmp = dict()
            continue

        contents = line.split("\t")
        key = contents[3].lower()
        if cur_start <= int(contents[1]) and cur_end >= int(contents[2]):
            tmp[key] = {"type": contents[4], "id": contents[5]}

        if cur_end < int(contents[1]) and len(tmp) > 1:
            tmp_list = list(tmp.items())
            for i, (tmp_key1, tmp_value1) in enumerate(tmp_list):
                if len(tmp_list) == i + 1:
                    break
                for j, (tmp_key2, tmp_value2) in enumerate(tmp_list[i+1:]):
                    if tmp_value1["type"] > tmp_value2["type"]:
                        relation_key = tmp_key1 + "~" + tmp_key2
                        relation_type = tmp_value1["type"] + "~" + tmp_value2["type"]
                    elif tmp_value1["type"] < tmp_value2["type"]:
                        relation_key = tmp_key2 + "~" + tmp_key1
                        relation_type = tmp_value2["type"] + "~" + tmp_value1["type"]
                    if relation_key not in relation.keys():
                        relation[relation_key] = {"count": 1, "type": relation_type}
                    else:
                        relation[relation_key]["count"] += 1

            tmp = dict()
            while True:
                cur_start += len(sentences[cur_index]) + 1
                cur_index += 1
                if cur_index == len(sentences):
                    break
                cur_end += len(sentences[cur_index]) + 1
                if cur_start <= int(contents[1]):
                    break

sorted_relation = sorted(relation.items(), key=lambda x: x[1]["count"])
for key, value in sorted_relation:
    if value["type"] == "Mutation~Gene" and value["count"] >= 0:
        key1, key2 = key.split("~")
        print(key1 + "\t" + key2 + "\t" + str(value["count"]))
# print(sorted_relation)
