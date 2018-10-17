import urllib
from nltk.parse.stanford import StanfordDependencyParser
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


def count_tag(pronoun, tag, tree):
    count = 0
    for triple in tree:
        if triple[1] == tag and triple[2][0] == pronoun:
            count += 1
    return count


def create_tree(triples):
    tree = []
    for triple in triples:
        tree.append(triple)
    return tree


def count_gender_subj_obj(tree):
    male_subj_count = count_tag("he", "nsubj", tree)
    male_obj_count = count_tag("him", "dobj", tree)
    female_subj_count = count_tag("she", "nsubj", tree)
    female_obj_count = count_tag("her", "dobj", tree)

    return (male_subj_count, male_obj_count, female_subj_count, female_obj_count)


if __name__ == "__main__":

    # create dependency parser
    path_to_jar = "assets/stanford-parser.jar"
    path_to_models_jar = "assets/stanford-parser-3.9.1-models.jar"
    load_jars(path_to_jar, path_to_models_jar)
    dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)


    sentences = {"She told him to pass the ball", "He told her words"}

    for sentence in sentences:
        result = dependency_parser.raw_parse(sentence.lower())
        parse = next(result)
        # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
        # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
        triples = list(parse.triples())
        tree = create_tree(triples)

        # print(count_tag("she", "nsubj", tree))

        print(count_gender_subj_obj(tree))
