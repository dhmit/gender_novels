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


def count_gender_subj_obj(tree):
    """
    This function takes in an dependency tree for a sentence and counts female and male subject and
    object occurences

    We have chosen not to include indirect object positions because whether or not they represent
    passivity (at least, compared to being a direct object) is debatable

    :param tree: An array which is a dependency tree
    :return: the counts of male and female subject and object occurences as a tuple of 4
    """

    male_subj_count = male_obj_count = female_subj_count = female_obj_count = 0
    for triple in tree:
        if triple[1] == "nsubj" and triple[2][0] == "he":
            male_subj_count += 1
        if triple[1] == "dobj" and triple[2][0] == "him":
            male_obj_count += 1
        if triple[1] == "nsubj" and triple[2][0] == "she":
            female_subj_count += 1
        if triple[1] == "dobj" and triple[2][0] == "her":
            female_subj_count += 1

    return (male_subj_count, male_obj_count, female_subj_count, female_obj_count)


def parse_sentence(sentence):
    """
    This function does all sentence parsing (we cannot split this up into separate functions for
    performance reasons (each additional function will require iterating over the entire tree again)
    :param sentence: sentence (string) we want to parse
    :return: the counts of male and female subject and object occurrences as a tuple of 4
    """
    result = dependency_parser.raw_parse(sentence.lower())
    parse = next(result)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    triples = list(parse.triples())
    tree = list(triples)
    return count_gender_subj_obj(tree)


def parse_novel(novel):
    """
    This function calls the parse_sentence function for all sentences in the novel
    :param novel: Novel object we want to analyze
    :return: the counts of male and female subject and object occurrences as a tuple of 4
    """
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
    # print(parse_novel(novel))

    sentences = {"She hit him before he could hit her back"}

    for sentence in sentences:
        result = dependency_parser.raw_parse(sentence.lower())
        parse = next(result)
        # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
        # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
        tree = list(parse.triples())
        print(sentence)
        print("--")
        print(parse.tree())
        print("--")
        print(count_gender_subj_obj(tree))
        print()
