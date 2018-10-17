import urllib
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize
from gender_novels.corpus import Corpus
import os.path

dependency_parser = None

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

def print_tree(tree):
    for triple in tree:
        print(triple)


def count_gender_subj_obj(tree):
    male_subj_count = count_tag("he", "nsubj", tree)
    male_obj_count = count_tag("him", "dobj", tree)
    female_subj_count = count_tag("she", "nsubj", tree)
    female_obj_count = count_tag("her", "dobj", tree)

    return (male_subj_count, male_obj_count, female_subj_count, female_obj_count)


def parse_sentence(sentence):
    result = dependency_parser.raw_parse(sentence.lower())
    parse = next(result)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    triples = list(parse.triples())
    tree = create_tree(triples)
    return count_gender_subj_obj(tree)


def parse_novel(novel):
    sentences = sent_tokenize(novel.text.replace("\n", " "))
    t_male_subj_count = t_male_obj_count = t_female_subj_count = t_female_obj_count = 0
    for sentence in sentences:
        (male_subj_count, male_obj_count, female_subj_count, female_obj_count) = parse_sentence(sentence)
        t_male_subj_count += male_subj_count
        t_male_obj_count += male_obj_count
        t_female_subj_count += female_subj_count
        t_female_obj_count += female_obj_count
        # print(sentence)
        # print cumulative counts
        print(t_male_subj_count, t_male_obj_count, t_female_subj_count, t_female_obj_count)
    return (t_male_subj_count, t_male_obj_count, t_female_subj_count, t_female_obj_count)


if __name__ == "__main__":

    # create dependency parser
    path_to_jar = "assets/stanford-parser.jar"
    path_to_models_jar = "assets/stanford-parser-3.9.1-models.jar"
    load_jars(path_to_jar, path_to_models_jar)
    dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)

    novels = Corpus('sample_novels').novels
    novel = novels[0]
    print(parse_novel(novel))

    # sentences = {"She told him to pass the ball",
    #              "He told something to her",
    #              "He gave her a gift",
    #              "The red dog sang a purple song for the blue cat",
    #              "The girl said that the man believes that the woman walked"}
    #
    # for sentence in sentences:
    #     result = dependency_parser.raw_parse(sentence.lower())
    #     parse = next(result)
    #     # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    #     # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    #     triples = list(parse.triples())
    #     tree = create_tree(triples)
    #
    #     # print(count_tag("she", "nsubj", tree))
    #
    #     print(sentence)
    #     print("--")
    #     print(parse.tree())
    #     print("--")
    #     print_tree(tree)
    #     print("--")
    #     print(count_gender_subj_obj(tree))
    #     print()
