"""
This file is intended for dependency parsing side tests.
"""

import urllib
from nltk.parse.stanford import StanfordDependencyParser
from gender_novels.corpus import Corpus
from nltk.tokenize import sent_tokenize

path_to_jar = "assets/stanford-parser.jar"
path_to_models_jar = "assets/stanford-parser-3.9.1-models.jar"

# The jar files are too big to commit directly, so download them
url_to_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser.jar"
url_to_models_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser-3.9.1-models.jar"
urllib.request.urlretrieve(url_to_jar, path_to_jar)
urllib.request.urlretrieve(url_to_models_jar, path_to_models_jar)

dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)

novels = Corpus('sample_novels').novels

for novel in novels:
    sentences = sent_tokenize(novel.text)
    print(sentences)

    result = dependency_parser.raw_parse_sents(sentences)

    for sentence in result:
        parse = next(sentence)
        # dependency tree
        # print("------DEPENDENCY TREE------")
        # print(parse.tree())
        # CoNLL format
        # print("------CONLL FORMAT------")
        # print(parse.to_conll(4))
        # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
        # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
        print("------DEPENDENCY TRIPLES------")
        triples = list(parse.triples())
        for triple in triples:
            print(triple)
        print()
