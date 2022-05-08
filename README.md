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

## 程序介绍

本项目包含以下代码文件：

- `entrez_access.py`：访问 Entrez API，获取文献 PMID；
- `pubtator_access.py`：访问 PubTator API，获取文献的标题和摘要标注；
- `entity_counter.py`：实体计数；
- `entity_relation.py`：共句关系计数；
- `relation_extraction.py`：三元组抽取；
- `DGL-KE_calling.py`：对 DGL-KE 的调用，实现了交叉验证和预测。

以上是长文（终稿）中涉及的代码实现。

