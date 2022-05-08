"""
共句分析
@author: zhang shilong
@date: 2022/04/05
"""
import re

input_path = "data/Covid-19_pubtator.txt"
output_path = "data/sentence.txt"
out = open(output_path, "w")
relation = {}

with open(input_path, "r", encoding="utf8") as file:
    text = file.read()
    articles = text.split("\n\n")

for article in articles:
    lines = article.split("\n")
    title = lines[0]
    if not title:
        continue
    title = title.split("|")[2]
    abstract = lines[1].split("|")[2]
    para = title + " " + abstract
    sep = [0]
    for pos in re.finditer("\. ", para):
        sep.append(int(pos.start())+2)

    annos = dict()
    for line in lines[2:]:
        if line:
            contents = line.strip("\n").split("\t")
            annos[int(contents[1])] = {"value": contents[3], "type": contents[4], "id": contents[5]}
    annos = list(annos.items())

    tmp = dict()
    cur_pos = 1
    cur_anno = 0
    while cur_pos < len(sep) and cur_anno < len(annos):
        if sep[cur_pos] >= annos[cur_anno][0]:
            if annos[cur_anno][1]["value"] not in tmp.keys():
                tmp[annos[cur_anno][1]["value"]] = {"type": annos[cur_anno][1]["type"], "id": annos[cur_anno][1]["id"]}
            cur_anno += 1

        if cur_anno == len(annos) or sep[cur_pos] <= annos[cur_anno][0]:
            if len(tmp) > 1:
                tmp_list = list(tmp.items())
                for i, (tmp_key1, tmp_value1) in enumerate(tmp_list):
                    if len(tmp_list) == i + 1:
                        break
                    for j, (tmp_key2, tmp_value2) in enumerate(tmp_list[i + 1:]):
                        flag = tmp_value1["type"] < tmp_value2["type"]
                        relation_key = tmp_key1 + "~" + tmp_key2 if flag else tmp_key2 + "~" + tmp_key1
                        relation_type = tmp_value1["type"] + "~" + tmp_value2["type"] \
                            if flag else tmp_value2["type"] + "~" + tmp_value1["type"]
                        if relation_key not in relation.keys():
                            relation[relation_key] = {"count": 1, "type": relation_type}
                        else:
                            relation[relation_key]["count"] += 1
                if relation_type == "Chemical~Gene":  # and relation_key.split("~")[0] == "tocilizumab":
                    out.write("s|" + para[sep[cur_pos-1]:sep[cur_pos]].encode('gbk', 'ignore').decode('gbk') + "\n")
                    line = []
                    for k, v in tmp.items():
                        line.append(v["type"] + ":" + k)
                    out.write("e|" + "\t".join(line).encode('gbk', 'ignore').decode('gbk') + "\n")
            cur_pos += 1
            tmp = dict()

# sorted_relation = sorted(relation.items(), key=lambda x: x[1]["count"])
# for k, v in sorted_relation:
#     if v["type"] == "Chemical~Gene" and k.split("~")[0] == "tocilizumab":
#         print("\t".join(k.split("~")) + "\t" + v["type"])
