import urllib
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize
from gender_novels.corpus import Corpus
from gender_novels.novel import Novel
import os.path
import time

def get_parser(path_to_jar, path_to_models_jar):
    """
    The jar files are too big to commit directly, so download them
    :param path_to_jar: local path to stanford-parser.jar
    :param path_to_models_jar: local path to stanford-parser-3.9.1-models.jar

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> parser == None
    False
    """

    url_to_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser.jar"
    url_to_models_jar = "http://www.trecento.com/dh_lab/nltk_jar/stanford-parser-3.9.1-models.jar"
    if not os.path.isfile(path_to_jar):
        urllib.request.urlretrieve(url_to_jar, path_to_jar)
    if not os.path.isfile(path_to_models_jar):
        urllib.request.urlretrieve(url_to_models_jar, path_to_models_jar)

    parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)
    return parser


def count_gender_subj_obj(tree):
    """
    This function takes in a tree of dependency triples for a list of sentence and counts female
    and male subject and object occurrences

    We have chosen not to include indirect object positions because whether or not they represent
    passivity (at least, compared to being a direct object) is debatable

    :param tree: A tree containing a list of dependency triples for each sentence
    :return: the counts of male and female subject and object occurrences as a tuple of 4

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> sentences = {"he told her", "she told him"}
    >>> result = parser.raw_parse_sents(sentences)
    >>> tree = list(result)
    >>> count_gender_subj_obj(tree)
    (1, 1, 1, 1)
    """

    male_subj_count = male_obj_count = female_subj_count = female_obj_count = 0
    for sentence in tree:
        for triple in next(sentence).triples():
            if triple[1] == "nsubj" and triple[2][0] == "he":
                male_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "him":
                male_obj_count += 1
            if triple[1] == "nsubj" and triple[2][0] == "she":
                female_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "her":
                female_obj_count += 1

    return (male_subj_count, male_obj_count, female_subj_count, female_obj_count)


def parse_novel(novel, parser):
    """
    This function calls the parse_sentence function for all sentences in the novel
    :param novel: Novel object we want to analyze
    :param parser: Stanford dependency parser
    :return: the counts of male and female subject and object occurrences as a tuple of 4

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> novels = Corpus('sample_novels').novels
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': None, 'text': "He told her"}
    >>> toy_novel = Novel(novel_metadata)
    >>> parse_novel(toy_novel, parser)
    (1, 0, 0, 1)

    """

    sentences = sent_tokenize(novel.text.lower().replace("\n", " "))
    result = parser.raw_parse_sents(sentences)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    tree = list(result)
    counts = count_gender_subj_obj(tree)
    return counts


def test_analysis():
    """
    This function contains all analysis code to be run (previously in main function)
    """

    parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")

    novels = Corpus('sample_novels').novels
    novel = novels[0]
    start = time.time()
    print(parse_novel(novel, parser))
    end = time.time()
    print(end-start)


if __name__ == "__main__":
    test_analysis()
