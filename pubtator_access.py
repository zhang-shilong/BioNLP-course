"""
调用PubTator API
@author: zhang shilong
@date: 2022/04/05
"""
import requests
import time

input_path = "data/Covid-19_pmid.txt"
output_path = "data/Covid-19_pubtator.txt"

with open(input_path, "r") as file:
    pmids = [pmid.strip() for pmid in file.readlines()]
out = open(output_path, "a+")

for pmid in pmids:
    r = requests.get("https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=" + pmid)
    if r.status_code != 200:
        print("[Error] PMID:" + pmid + "  HTTP code:" + str(r.status_code))
        continue
    out.write(r.text)
    time.sleep(0.3)

out.close()
