import urllib
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize, word_tokenize
from gender_novels.corpus import Corpus
from gender_novels.novel import Novel
from gender_novels.common import store_pickle, load_pickle
import os.path
import csv

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


def pickle(novel, parser):
    """
    This function returns a pickled tree
    :param novel: Novel we are interested in
    :param parser: Stanford parser object
    :return: tree in pickle format

    >>> tree = load_pickle(f'dep_tree_aanrud_longfrock')
    >>> tree == None
    False
    """

    try:
        tree = load_pickle(f'dep_tree_{str(novel)}')
    except (IOError, FileNotFoundError):
        sentences = sent_tokenize(novel.text.lower().replace("\n", " "))
        he_she_sentences = []
        for sentence in sentences:
            add_sentence = False
            words = [word for word in word_tokenize(sentence)]
            for word in words:
                if word == "he" or word == "she" or word == "him" or word == "her":
                    add_sentence = True
            if add_sentence:
                he_she_sentences.append(sentence)
        sentences = he_she_sentences
        result = parser.raw_parse_sents(sentences)
        # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
        # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
        tree = list(result)
        tree_list = []
        i = 0
        for sentence in tree:
            tree_list.append([])
            triples = list(next(sentence).triples())
            for triple in triples:
                tree_list[i].append(triple)
            i += 1
        tree = tree_list
        store_pickle(tree, f'dep_tree_{str(novel)}')
    return tree


def parse_novel(novel, parser):
    """
    This function parses all sentences in the novel
    :param novel: Novel object we want to analyze
    :param parser: Stanford dependency parser
    :return: list containing the following:
    - Title of novel
    - Count of male pronoun subject occurrences
    - Count of male pronoun object occurrences
    - Count of female pronoun subject occurrences
    - Count of female pronoun object occurrences
    - List of adjectives describing male pronouns as one space-separated string
    - List of verbs associated with male pronouns as one space-separated string
    - List of adjectives describing female pronouns as one space-separated string
    - List of verbs associated with female pronouns as one space-separated string

    >>> parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")
    >>> novels = Corpus('sample_novels').novels
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': None, 'text': "He told her"}
    >>> toy_novel = Novel(novel_metadata)
    >>> parse_novel(toy_novel, parser)
    ('Scarlet Letter', 1, 0, 0, 1, [], ['told'], [], [])

    """

    tree = pickle(novel, parser)
    male_subj_count = male_obj_count = female_subj_count = female_obj_count = 0
    female_adjectives = []
    male_adjectives = []
    female_verbs = []
    male_verbs = []

    for sentence in tree:
        for triple in sentence:
            if triple[1] == "nsubj" and triple[2][0] == "he":
                male_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "him":
                male_obj_count += 1
            if triple[1] == "nsubj" and triple[2][0] == "she":
                female_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "her":
                female_obj_count += 1
            if triple[1] == "nsubj" and triple[0][1] == "JJ":
                if triple[2][0] == "she":
                    female_adjectives.append(triple[0][0])
                elif triple[2][0] == "he":
                    male_adjectives.append(triple[0][0])
            if triple[1] == "nsubj" and (triple[0][1] == "VBD" or triple[0][1] == "VB" or
                                         triple[0][1] == "VBP" or triple[0][1] == "VBZ"):
                if triple[2][0] == "she":
                    female_verbs.append(triple[0][0])
                elif triple[2][0] == "he":
                    male_verbs.append(triple[0][0])

    return [novel.title, male_subj_count, male_obj_count, female_subj_count, female_obj_count,
            " ".join(male_adjectives), " ".join(male_verbs), " ".join(female_adjectives),
            " ".join(female_verbs)]


def test_analysis():
    """
    This function contains all analysis code to be run (previously in main function)
    - First generates a Stanford NLP parser
    - Iterates over sample novels corpus and parses each novel (performs analysis: gender pronoun
    count, list of adjectives, list of verbs)
    - Writes output to dependency_analysis_results.csv
    """

    parser = get_parser("assets/stanford-parser.jar", "assets/stanford-parser-3.9.1-models.jar")
    novels = Corpus('sample_novels').novels
    for novel in novels:
        try:
            row = parse_novel(novel, parser)
            print(row)
            with open('dependency_analysis_results.csv', mode='w') as results_file:
                writer = csv.writer(results_file, delimiter=',', quotechar='"',
                                             quoting=csv.QUOTE_MINIMAL)
                writer.writerow(row)
        except OSError:
            continue

if __name__ == "__main__":

    test_analysis()
