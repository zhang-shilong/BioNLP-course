"""
通过Entrez获取pmid
@author: zhang shilong
@date: 2022/04/05
"""
from Bio import Entrez

term = "Covid-19"
Entrez.email = "zhang_shilong@outlook.com"
search_results = Entrez.read(
    Entrez.esearch(db="pubmed", term=term, retmax=300000, datatype="pdat", mindate="2021/07/01", maxdate="2022/03/01")
)
with open("data/" + term + "_pmid.txt", "w") as out:
    out.write("\n".join(search_results["IdList"]))
