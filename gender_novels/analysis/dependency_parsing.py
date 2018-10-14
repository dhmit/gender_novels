"""
This file is intended for dependency parsing side tests.
"""

import pprint

from nltk.parse.stanford import StanfordDependencyParser

path_to_jar = "assets/stanford-parser.jar"
path_to_models_jar = "assets/stanford-parser-3.9.1-models.jar"

dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar,
                                             path_to_models_jar=path_to_models_jar)

"""
Parse one sentence at a time
"""

# result = dependency_parser.raw_parse('He walked by her')
# parsed = next(result)
# print(parsed.tree())
# triples = list(parsed.triples())
# for triple in triples:
#     print(triple)

"""
Parse multiple sentences at a time
"""

sentences = ["The quick brown fox jumped over the lazy dog",
             "He walked with her",
             "He walked by her",
             "I'm not going to tell you about her",
             "She has two rooms",
             "She was brave",
             "He hit her"]

result2 = dependency_parser.raw_parse_sents(sentences)

for sentence in result2:
    parse = next(sentence)
    # dependency tree
    print("------DEPENDENCY TREE------")
    print(parse.tree())
    # CoNLL format
    print("------CONLL FORMAT------")
    print(parse.to_conll(4))
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    print("------DEPENDENCY TRIPLES------")
    triples = list(parse.triples())
    for triple in triples:
        print(triple)
    print()
