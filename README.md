# BioNLP-course

这里是第 2 组，选题为《图表示学习在 Covid-19 文献挖掘和知识发现中的应用》，通过以下步骤，您可以快速地了解或再现我们的实验。

## 环境安装

我们所用的环境是 Python 3.7.13。

通过 `requirements.txt` 下载我们所用的 Python 库与 spaCy 模型。其中 en_core_web_sm 仅用于对比，实验中实际使用的的模型是 en_core_sci_sm。

```shell
conda create -n bionlp python=3.7.13
conda activate bionlp
pip install -r requirements.txt
# python -m spacy download en_core_web_sm
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz
```

## 文献 PMID 获取

以“Covid-19”为检索条目，要求出版时间为 2021 年 7 月 1 日至 2022 年 3 月 1 日，从 Entrez 获取 PMID，输出到 `Covid-19_pmid.txt`。

```shell
python entrez_access.py
```

## PubTator 实体标注

调用 PubTator API，从 PubTator 检索 PMID，获取标题、摘要和实体标注信息，输出到 `Covid-19_pubtator`。

```shell
python pubtator_access.py
```

## 实体频次统计

统计实体频次。

```shell
python entity_count.py
```

## 共句分析

我们对 PubTator 标注的实体进行共句分析，期望找到基因和 Covid-19 突变类型的关系，并将结果输出为 Cytoscape 可以读取的信息，进行可视化。

```shell
python entity_relation.py
```

## 小结

以上是长文（修订稿）中涉及的代码实现。

