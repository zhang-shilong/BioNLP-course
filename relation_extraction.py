"""
关系抽取
@author: zhang shilong
@date: 2022/04/16
"""
import spacy
from spacy import displacy
import scispacy
import networkx as nx
import matplotlib.pyplot as plt
import re

def split_W(entity):
    # split by non-alphabet and non-number characters
    tmp = re.split("\W", entity.lower())
    return max(tmp, key=len, default="")

def get_name_in_graph(graph, name):
    # get the name actually existing in the graph
    if name in graph.nodes():
        return name
    for node in graph.nodes():
        if name in node:
            return node

def add_modifers(graph, path, addition=list()):
    # add modifers for finded shortest path
    path.insert(0, "")
    path.append("")
    path_with_modifers = path.copy()
    j = 0
    for node in path[2:-2]:
        j += 1
        if not node:
            continue
        # sort by dependence relation, n*** words always appear before their dependent in natural language
        sorted_node = sorted(graph[node].items(), key=lambda x:x[1]["type"])
        for id, type in sorted_node:
            if id not in path and id not in addition:
                if type["type"] in ["amod", "advmod"]:
                    path_with_modifers.insert(j, id)
                    j += 1
                elif type["type"] in ["nsubj", "nmod"]:
                    path_with_modifers.insert(j + 1, id)
                    j += 1
    return path_with_modifers

def find_common_neighbor(graph, entity_dict, e, expect):
    # find the first common neighbor with near type in the rest of entities expect e
    neighbor1 = set(graph[e].keys())
    for entity in entity_dict.keys():
        if entity != expect and  entity_dict[e] == entity_dict[entity]:
            neighbor2 = set(graph[entity].keys())
            inter = list(neighbor1 & neighbor2)
            if inter and \
                    ((graph.edges[e, inter[0]]["type"] in ["nsubj", "nsubjpass"] and graph.edges[entity, inter[0]]["type"] in ["nmod"])\
                    or (graph.edges[e, inter[0]]["type"] in ["nmod"] and graph.edges[entity, inter[0]]["type"] in ["nsubj", "nsubjpass"])):
                return inter[0]
    return ""

def back_to_raw_name(raw_dict, path):
    # replace entity name in path
    path = " ".join(path[1:-1])
    for pv, v in raw_dict.items():
        path = path.replace(pv ,v)
    print(path)

def sdp(graph, entity_dict, entity_list, raw_dict):
    # algorithm of shortest dependency path, including nx.shortest_path() and add_modifers(), output processed SDP
    for i, e1 in enumerate(entity_list):
        for e2 in entity_list[i+1:]:
            common = find_common_neighbor(graph, entity_dict, e1, e2)
            if common:
                path = add_modifers(graph, nx.shortest_path(graph, source=common, target=e2), addition=[e1, e2])
                path.insert(1, e1)
                back_to_raw_name(raw_dict, path)
            else:
                path = add_modifers(graph, nx.shortest_path(graph, source=e1, target=e2))
                back_to_raw_name(raw_dict, path)

if __name__ == "__main__":
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_sci_sm")  # ScispaCy model for biomedical text

    with open("data/sentence.txt", "r") as file:
        for line in file.readlines():
            line = line.strip("\n")
            if line.startswith("s|"):
                text = line[2:]
                if ": " in text[:15]:
                    # if exists text like BACKGROUND:/AIM:/RESULTS:/etc, which result in wrong dependency tree
                    text = text.split(": ")[1]
                doc = nlp(text)
                # displacy.serve(doc, style="dep")

                # generate NetworkX graph
                graph = nx.Graph()
                for token in doc:
                    for child in token.children:
                        graph.add_edge(token.lower_, child.lower_, type=child.dep_)
                # nx.draw(graph, with_labels=True)
                # plt.show()

            elif line.startswith("e|"):
                raw_entities = dict()
                entities_dict = dict()
                for pair in line[2:].split("\t"):
                    k, v = pair.split(":", 1)
                    pv = get_name_in_graph(graph, split_W(v))
                    if pv:
                        entities_dict[pv] = k
                        raw_entities[pv] = v
                entities_list = list(entities_dict.keys())

                sdp(graph, entities_dict, entities_list, raw_entities)
