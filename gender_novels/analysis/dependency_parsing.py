import urllib
from nltk.parse.stanford import StanfordDependencyParser
from gender_novels.corpus import Corpus
from nltk.tokenize import sent_tokenize
import os.path

def load_jars(path_to_jar, path_to_models_jar):
    """
    The jar files are too big to commit directly, so download them
    :param path_to_jar: local path to stanford-parser.jar
    :param path_to_models_jar: local path to stanford-parser-3.9.1-models.jar
    """
    url_to_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser.jar"
    url_to_models_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser-3.9.1-models.jar"
    if not os.path.isfile(path_to_jar):
        urllib.request.urlretrieve(url_to_jar, path_to_jar)
    if not os.path.isfile(path_to_models_jar):
        urllib.request.urlretrieve(url_to_models_jar, path_to_models_jar)

if __name__ == "__main__":

    # create dependency parser
    path_to_jar = "assets/stanford-parser.jar"
    path_to_models_jar = "assets/stanford-parser-3.9.1-models.jar"
    load_jars(path_to_jar, path_to_models_jar)
    dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)

    sentence = "She told him to pass the ball"
    result = dependency_parser.raw_parse(sentence)

    parse = next(result)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    print("------DEPENDENCY TRIPLES------")
    triples = list(parse.triples())
    for triple in triples:
        print(triple)
    print()
