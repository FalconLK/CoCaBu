# CoCaBu
Code search engine for java programming language.
http://code-search.uni.lu/cocabu

## What it is?
CoCaBu is a code search engine that resolves the vocabulary mismatch problem. While other code search engines directly match user queries and source code, our engine translates and augments user queries into code-friendly queries. This process can improve code search results.

## How it works?
Input: Free-form text.
CoCaBu works based on open source java code from a super repository, GitHub and a Q & A posts from Stackoverflow. Once you ask a question to CoCaBu, it will retrieve code related to your question by leveraging Stackoverflow posts. 

## How to run it?
CoCaBu is jython based implementation. Since the size of data, we are preparing a virtual machine. 

## Maintance
@FalconLK Kisub Kim
@darksw Dongsun Kim
@Deadlyelder Sankalp

## Citation
```
@inproceedings{sirres2018augmenting,
  title={Augmenting and structuring user queries to support efficient free-form code search},
  author={Sirres, Raphael and Bissyand{\'e}, Tegawend{\'e} F and Kim, Dongsun and Lo, David and Klein, Jacques and Kim, Kisub and Traon, Yves Le},
  booktitle={Proceedings of the 40th International Conference on Software Engineering},
  pages={945--945},
  year={2018},
  organization={ACM}
}```
