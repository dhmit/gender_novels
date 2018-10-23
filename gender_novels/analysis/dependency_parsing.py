import urllib
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize
from gender_novels.corpus import Corpus
from gender_novels.novel import Novel
import os.path

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
    >>> sentence = "She hit him first"
    >>> result = parser.raw_parse(sentence.lower())
    >>> parse = next(result)
    >>> triples = list(parse.triples())
    >>> count_gender_subj_obj(triples)
    (0, 1, 1, 0)
    """

    male_subj_count = male_obj_count = female_subj_count = female_obj_count = 0
    print(tree)
    for sentence in tree:
        print(sentence)
        for triple in next(sentence).triples():
            print(triple)
            print(triple[1])
            if triple[1] == "nsubj" and triple[2][0] == "he":
                male_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "him":
                male_obj_count += 1
            if triple[1] == "nsubj" and triple[2][0] == "she":
                female_subj_count += 1
            if triple[1] == "dobj" and triple[2][0] == "her":
                female_subj_count += 1

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
    (1, 0, 1, 0)

    """

    sentences = sent_tokenize(novel.text.lower().replace("\n", " "))
    result = parser.raw_parse_sents(sentences)
    # dependency triples of the form ((head word, head tag), rel, (dep word, dep tag))
    # link defining dependencies: https://nlp.stanford.edu/software/dependencies_manual.pdf
    tree = list(result)
    t_male_subj_count = t_male_obj_count = t_female_subj_count = t_female_obj_count = count_gender_subj_obj(tree)
    return (t_male_subj_count, t_male_obj_count, t_female_subj_count, t_female_obj_count)


def test_analysis():
    """
    This function contains all analysis code to be run (previously in main function)
    """

    parser = get_parser("assets/stanford-parser.jar","assets/stanford-parser-3.9.1-models.jar")

    # novels = Corpus('sample_novels').novels
    # novel = novels[0]
    novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
                      'corpus_name': 'sample_novels', 'date': '1900', 'filename': None,
                      'text': "But to leave his post as watchman was not to be thought of just "
                              "now, for the pigs and the goats were out to-day. At this moment "
                              "they were busy with their separate affairs and behaving very well,"
                              "--the pigs over on the sunny side of the dooryard scratching "
                              "themselves against the corner of the cow house, and the goats "
                              "gnawing bark from the big heap of pine branches that had been laid "
                              "near the sheep barn for their special use. They looked as if they "
                              "thought of nothing but their scratching and gnawing; but "
                              "Bearhunter knew well, from previous experience, that no sooner "
                              "would he go into the house than both pigs and goats would come "
                              "rushing over to the doorway and do all the mischief they could. "
                              "That big goat, Crookhorn,--the new one who had come to the farm "
                              "last autumn and whom Bearhunter had not yet brought under "
                              "discipline,--had already strayed in a roundabout way to the very "
                              "corner of the farmhouse, and was looking at Bearhunter in a"
                              "self-important manner, as if she did not fear him in the least. "
                              "She was really an intolerable creature, that goat Crookhorn! But "
                              "just let her dare--!"}
    toy_novel = Novel(novel_metadata)
    print(parse_novel(toy_novel, parser))


if __name__ == "__main__":
    test_analysis()
