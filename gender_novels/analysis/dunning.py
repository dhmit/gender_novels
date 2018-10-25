import pickle
import math
from operator import itemgetter
from gender_novels.corpus import Corpus
from scipy.stats import chi2
from gender_novels.common import store_pickle, load_pickle
import unittest
import nltk
from collections import Counter



def dunn_individual_word(total_words_corpus_1, total_words_corpus_2, count_of_word_corpus_1,
                         count_of_word_corpus_2):
    '''
    applies dunning log likelihood to compare individual word in two counter objects

    :param word: desired word to compare
    :param m_corpus: c.filter_by_gender('male')
    :param f_corpus: c. filter_by_gender('female')
    :return: log likelihoods and p value
    >>> total_words_m_corpus = 8648489
    >>> total_words_f_corpus = 8700765
    >>> wordcount_female = 1000
    >>> wordcount_male = 50
    >>> dunn_individual_word(total_words_m_corpus,total_words_f_corpus,wordcount_male,wordcount_female)

    '''
    a = count_of_word_corpus_1
    b = count_of_word_corpus_2
    c = total_words_corpus_1
    d = total_words_corpus_2

    e1 = c * (a + b) / (c + d)
    e2 = d * (a + b) / (c + d)

    dunning_log_likelihood = 2 * (a * math.log(a / e1) + b * math.log(b / e2))

    if count_of_word_corpus_1 * math.log(count_of_word_corpus_1 / e1) < 0:
        dunning_log_likelihood = -dunning_log_likelihood

    p = 1 - chi2.cdf(abs(dunning_log_likelihood),1)

    return dunning_log_likelihood

def dunning_total(counter1, counter2, filename_to_pickle=None):
    '''
    runs dunning_individual on words shared by both counter objects
    (-) end of spectrum is words for counter_2
    (+) end of spectrum is words for counter_1
    the larger the magnitude of the number, the more distinctive that word is in its
    respective counter object

    use filename_to_pickle to store the result so it only has to be calculated once and can be
    used for multiple analyses.

    >>> from collections import Counter
    >>> female_counter = Counter({'he': 1,  'she': 10, 'and': 10})
    >>> male_counter =   Counter({'he': 10, 'she': 1,  'and': 10})
    >>> results = dunning_total(female_counter, male_counter)

    # Results is a dict that maps from terms to results
    # Each result dict contains the dunning score...
    >>> results['he']['dunning']
    -8.547243830635558

    # ... counts for corpora 1 and 2 as well as total count
    >>> results['he']['count_total'], results['he']['count_corp1'], results['he']['count_corp2']
    (11, 1, 10)

    # ... and the same for frequencies
    >>> results['he']['freq_total'], results['he']['freq_corp1'], results['he']['freq_corp2']
    (0.2619047619047619, 0.047619047619047616, 0.47619047619047616)

    :return: dict

    '''

    total_words_counter1 = 0
    total_words_counter2 = 0

    #get word total in respective counters
    for word1 in counter1:
        total_words_counter1 += counter1[word1]
    for word2 in  counter2:
        total_words_counter2 += counter2[word2]

    #dictionary where results will be returned
    dunning_result = {}
    for word in counter1:
        counter1_wordcount = counter1[word]
        if word in counter2:
            counter2_wordcount = counter2[word]

            if counter1_wordcount + counter2_wordcount < 10:
                continue

            dunning_word = dunn_individual_word( total_words_counter1,  total_words_counter2,
                                                 counter1_wordcount,counter2_wordcount)
            dunning_result[word] = {
                'dunning': dunning_word,
                'count_total': counter1_wordcount + counter2_wordcount,
                'count_corp1': counter1_wordcount,
                'count_corp2': counter2_wordcount,
                'freq_total': (counter1_wordcount + counter2_wordcount) / (total_words_counter1 +
                                                                           total_words_counter2),
                'freq_corp1': counter1_wordcount / total_words_counter1,
                'freq_corp2': counter2_wordcount / total_words_counter2
            }

    if filename_to_pickle:
        store_pickle(dunning_result, filename_to_pickle)

    return dunning_result


def dunning_result_displayer(dunning_result, number_of_terms_to_display=10,
                             part_of_speech_to_include=None):
    """
    Convenience function to display dunning results as tables.

    part_of_speech_to_include can either be a list of POS tags or a 'adjectives, 'adverbs',
    'verbs', or 'pronouns'. If it is None, all terms are included.

    :return:
    """
    #TODO: heading says Corpus 1 and Corpus 2 which is confusing when the two counters are for different words from the
    # same corpus.  fix this

    pos_names_to_tags = {
        'adjectives':   ['JJ', 'JJR', 'JJS'],
        'adverbs':      ['RB', 'RBR', 'RBS', 'WRB'],
        'verbs':        ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
        'pronouns':     ['PRP', 'PRP$', 'WP', 'WP$']
    }
    if part_of_speech_to_include in pos_names_to_tags:
        part_of_speech_to_include = pos_names_to_tags[part_of_speech_to_include]


    headings = ['term', 'dunning', 'count_total', 'count_corp1', 'count_corp2', 'freq_total',
                'freq_corp1', 'freq_corp2']

    output = f'\nDisplaying Part of Speech: {part_of_speech_to_include}\n'
    for i in range(1,3):
        output += f'\nDunning Log-Likelihood results for Corpus {i}\n|'

        for heading in headings:
            output += '  {:13s}|'.format(heading)
        output += '\n' + 8 * 16 * '_' + '\n'

        reverse = False
        if i == 2: reverse = True
        sorted_results = sorted(dunning_result.items(), key=lambda x: x[1]['dunning'],
                                reverse=reverse)
        count_displayed = 0
        for result in sorted_results:
            if count_displayed == number_of_terms_to_display:
                break
            term = result[0]
            term_pos = nltk.pos_tag([term])[0][1]
            if part_of_speech_to_include and term_pos not in part_of_speech_to_include:
                continue

            output += '|  {:13s}|'.format(result[0])
            for heading in headings[1:]:

                if heading in ['freq_total', 'freq_corp1', 'freq_corp2']:
                    output += '  {:11.4f}% |'.format(result[1][heading] * 100)
                elif heading in ['dunning']:
                    output += '  {:12.2f} |'.format(result[1][heading])
                else:
                    output += '  {:12.0f} |'.format(result[1][heading])
            output += '\n'
            count_displayed += 1

    print(output)



def male_VS_female_analysis_dunning(corpus_name):
    '''
    tests word distinctiveness of shared words between male and female corpora using dunning
    Prints out the most distinctive terms overall as well as grouped by verbs, adjectives etc.

    :return: dict # from Mingfei: does this function actually return anything?
    '''


    # By default, try to load precomputed results. Only calculate if no stored results are
    # available.
    pickle_filename = f'dunning_male_vs_female_authors_{corpus_name}'
    try:
        results = load_pickle(pickle_filename)
    except IOError:

        c = Corpus(corpus_name)
        m_corpus = c.filter_by_gender('male')
        f_corpus = c.filter_by_gender('female')
        wordcounter_male = m_corpus.get_wordcount_counter()
        wordcounter_female = f_corpus.get_wordcount_counter()
        results = dunning_total(wordcounter_male, wordcounter_female,
                                filename_to_pickle=pickle_filename)

    for group in [None, 'verbs', 'adjectives', 'pronouns', 'adverbs']:
        dunning_result_displayer(results, number_of_terms_to_display= 50,
                                 part_of_speech_to_include=group)


def compare_word_association_in_corpus_analysis_dunning(word1, word2, corpus = None, corpus_name = None):
    """
    Uses Dunning analysis to compare words associated with word1 vs words associated with word2 in
    the Corpus passed in as the parameter.  If a corpus and corpus_name are passsed in, then the
    analysis will use the corpus but name the file after corpus_name.  If no corpus is passed in but
    a corpus_name is, then the method will try to create a Corpus by corpus = Corpus(corpus_name).
    If neither a corpus nor a corpus_name is passed in, analysis is simply done on the Gutenberg
    corpus.

    :param word1: str
    :param word2: str
    :param corpus: Corpus
    :param corpus_name: str
    :return: dict
    """

    if corpus:
        if not corpus_name:
            corpus_name = corpus.corpus_name
    else:
        if not corpus_name:
            corpus_name = "gutenberg"
        corpus = Corpus(corpus_name)

    pickle_filename = f'dunning_{word1}_vs_{word2}_associated_words_{corpus_name}'
    try:
        results = load_pickle(pickle_filename)
    except IOError:
        try:
            pickle_filename = f'dunning_{word2}_vs_{word1}_associated_words_{corpus_name}'
            results = load_pickle(pickle_filename)
        except:
            word1_counter = Counter()
            word2_counter = Counter()
            for novel in corpus.novels:
                word1_counter.update(novel.words_associated(word1))
                word2_counter.update(novel.words_associated(word2))
            results = dunning_total(word1_counter, word2_counter, filename_to_pickle=pickle_filename)

    for group in [None, 'verbs', 'adjectives', 'pronouns', 'adverbs']:
        dunning_result_displayer(results, number_of_terms_to_display=50,
                                 part_of_speech_to_include=group)

    return results

def he_vs_she_associations_analysis_dunning(corpus, corpus_name = None):
    """
    Uses Dunning analysis to compare words associated with 'he' vs words associated with 'she' in
    the Corpus passed in as the parameter.  The corpus_name parameter is if you want to name the file
    something other than Gutenberg (e.g. Gutenberg_female_authors)
    :param corpus: Corpus
    :param corpus_name: str
    :return: dict
    """

    if not corpus_name:
        corpus_name = corpus.corpus_name

    pickle_filename = f'dunning_he_vs_she_associated_words_{corpus_name}'
    try:
        results = load_pickle(pickle_filename)
    except IOError:
        he_counter = Counter()
        she_counter = Counter()
        for novel in corpus.novels:
            he_counter.update(novel.words_associated("he"))
            she_counter.update(novel.words_associated("she"))
        results = dunning_total(he_counter, she_counter, filename_to_pickle=pickle_filename)

    for group in [None, 'verbs', 'adjectives', 'pronouns', 'adverbs']:
        dunning_result_displayer(results, number_of_terms_to_display= 50,
                                 part_of_speech_to_include=group)

    return results


def he_vs_she_associations_analysis_dunning_gutenberg():
    """
    Uses Dunning analysis to compare words associated with 'he' vs words associated with 'she' in
    the Gutenberg corpus.
    :return: dict
    """
    gutenberg = Corpus("gutenberg")
    return he_vs_she_associations_analysis_dunning(gutenberg, "gutenberg")


def compare_word_association_between_corpus_analysis_dunning(word, corpus1 = None, corpus1_name = None, corpus2 = None, corpus2_name = None):
    """
    Uses Dunning analysis to compare words associated with word between corpuses.  If a corpus and corpus_name are
    passsed in, then the analysis will use the corpus but name the file after corpus_name.  If no corpus is passed in but
    a corpus_name is, then the method will try to create a Corpus by corpus = Corpus(corpus_name).
    If neither a corpus nor a corpus_name is passed in, analysis is simply done on the Gutenberg
    corpus.

    :param word1: str
    :param word2: str
    :param corpus: Corpus
    :param corpus_name: str
    :return: dict
    """

    if corpus1:
        if not corpus1_name:
            corpus1_name = corpus1.corpus_name
    else:
        if not corpus1_name:
            corpus1_name = "gutenberg"
        corpus1 = Corpus(corpus1_name)
        
    if corpus2:
        if not corpus2_name:
            corpus2_name = corpus2.corpus_name
    else:
        if not corpus2_name:
            corpus2_name = "gutenberg"
        corpus2 = Corpus(corpus2_name)

    pickle_filename = f'dunning_{word}_associated_words_{corpus1_name}_vs_{corpus2_name}'
    try:
        results = load_pickle(pickle_filename)
    except IOError:
        try:
            pickle_filename = f'dunning_{word}_associated_words_{corpus2_name}_vs_{corpus1_name}'
            results = load_pickle(pickle_filename)
        except:
            print("Analysis starting...")
            corpus1_counter = Counter()
            corpus2_counter = Counter()
            for novel in corpus1.novels:
                corpus1_counter.update(novel.words_associated(word))
            for novel in corpus2.novels:
                corpus2_counter.update(novel.words_associated(word))
            results = dunning_total(corpus1_counter, corpus2_counter, filename_to_pickle=pickle_filename)

    for group in [None, 'verbs', 'adjectives', 'pronouns', 'adverbs']:
        dunning_result_displayer(results, number_of_terms_to_display=50,
                                 part_of_speech_to_include=group)

    return results


if __name__ == '__main__':

    # male_VS_female_analysis_dunning('gutenberg')

    # sample_novels = Corpus("sample_novels")
    # he_vs_she_associations_analysis_dunning(sample_novels)

    male_corpus = Corpus("sample_novels").filter_by_gender("male")
    female_corpus = Corpus("sample_novels").filter_by_gender("female")
    compare_word_association_between_corpus_analysis_dunning("he", corpus1=male_corpus, corpus1_name="sample_male_authors",
                                                             corpus2=female_corpus, corpus2_name= "sample_female_authors")
