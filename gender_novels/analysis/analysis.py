"""
This file is intended for individual analyses of the gender_novels project
"""

from gender_novels.corpus import Corpus
from gender_novels.novel import Novel
import nltk
import math
from operator import itemgetter
nltk.download('stopwords', quiet=True)
#TODO: add prior two lines to setup, necessary to run
import collections
from scipy.stats import chi2
from statistics import mean, median, mode
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

import numpy as np
#import matplotlib.pyplot as plt


def test_function():
    d = {"Austin": [.5, .5], "Elliot": [.8, .2], "Sam": [.14, .22]}
    display_gender_freq(d=d, title="he_she_freq")  # made up data that works


def get_count_words(novel, words):
    """
    Takes in novel, a Novel object, and words, a list of words to be counted.
    Returns a dictionary where the keys are the elements of 'words' list
    and the values are the numbers of occurences of the elements in the novel.
    N.B.: Not case-sensitive.
    >>> from gender_novels import novel
    >>> summary = "Hester was convicted of adultery. "
    >>> summary += "which made her very sad, and then Arthur was also sad, and everybody was "
    >>> summary += "sad and then Arthur died and it was very sad.  Sadness."
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1850',
    ...                   'filename': None, 'text': summary}
    >>> scarlett = novel.Novel(novel_metadata)
    >>> get_count_words(scarlett, ["sad", "and"])
    {'sad': 4, 'and': 4}

    :param:words: a list of words to be counted in text
    :return: a dictionary where the key is the word and the value is the count
    """
    dic_word_counts = {}
    for word in words:
        dic_word_counts[word] = novel.get_count_of_word(word)
    return dic_word_counts


def get_comparative_word_freq(freqs):
    """
    Returns a dictionary of the frequency of words counted relative to each other.
    If frequency passed in is zero, returns zero

    :param freqs: dictionary
    :return: dictionary

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': 'hawthorne_scarlet.txt'}
    >>> scarlet = novel.Novel(novel_metadata)
    >>> d = {'he':scarlet.get_word_freq('he'), 'she':scarlet.get_word_freq('she')}
    >>> d
    {'he': 0.007329554965683813, 'she': 0.005894731807638042}
    >>> x = get_comparative_word_freq(d)
    >>> x
    {'he': 0.554249547920434, 'she': 0.445750452079566}
    >>> d2 = {'he': 0, 'she': 0}
    >>> d2
    {'he': 0, 'she': 0}
    """

    total_freq = sum(freqs.values())
    comp_freqs = {}

    for k, v in freqs.items():
        try:
            freq = v / total_freq
        except ZeroDivisionError:
            freq = 0
        comp_freqs[k] = freq

    return comp_freqs


def get_counts_by_pos(freqs):
    """
    This functions returns a dictionary where each key is a part of speech tag (e.g. 'NN' for nouns)
    and the value is a counter object of words of that part of speech and their frequencies.
    It also filters out words like "is", "the". We used `nltk`'s stop words function for filtering.
    
    >>> get_counts_by_pos(collections.Counter({'baked':1,'chair':3,'swimming':4}))
    {'VBN': Counter({'baked': 1}), 'NN': Counter({'chair': 3}), 'VBG': Counter({'swimming': 4})}
    >>> get_counts_by_pos(collections.Counter({'is':10,'usually':7,'quietly':42}))
    {'RB': Counter({'quietly': 42, 'usually': 7})}

    :param freqs:
    :return:
    """

    sorted_words = {}
    # for each word in the counter
    for word in freqs.keys():
        # filter out if in nltk's list of stop words, e.g. is, the
        if word not in stop_words:
            # get its part of speech tag from nltk's pos_tag function
            tag = nltk.pos_tag([word])[0][1]
            # add that word to the counter object in the relevant dict entry
            if tag not in sorted_words.keys():
                sorted_words[tag] = collections.Counter({word:freqs[word]})
            else:
                sorted_words[tag].update({word:freqs[word]})
    return sorted_words

def display_gender_freq(d, title):
    """
    Takes in a dictionary sorted by author and gender frequencies, and a title.
    Outputs the resulting graph to 'visualizations/title.pdf' AND 'visualizations/title.png'
    dictionary format {"Author/Novel": [he_freq, she_freq]}

    Will scale to allow inputs of larger dictionaries with non-binary values

    :param d, title:
    :return:
    """
    he_val = []
    she_val = []
    authors = []

    for entry in d:
        authors.append(entry)
        he_val.append(d[entry][0])
        she_val.append(d[entry][1])

    fig, ax = plt.subplots()

    index = np.arange(len(d.keys()))
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    he_val = tuple(he_val)
    she_val = tuple(she_val)
    authors = tuple(authors)

    rects1 = ax.bar(index, he_val, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    label='He')

    rects2 = ax.bar(index + bar_width, she_val, bar_width,
                    alpha=opacity, color='r',
                    error_kw=error_config,
                    label='She')

    ax.set_xlabel('Authors')
    ax.set_ylabel('Frequency')
    ax.set_title('Gendered Pronouns by Author')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(authors)
    ax.legend()

    fig.tight_layout()
    #plt.show()
    filepng = "visualizations/" + title + ".png"
    filepdf = "visualizations/" + title + ".pdf"
    plt.savefig(filepng, bbox_inches='tight')
    plt.savefig(filepdf, bbox_inches='tight')

def dunn_individual_word(total_words_m_corpus, total_words_f_corpus, wordcount_female,
                         wordcount_male):

    '''
    applies dunning log likelihood to compare individual word usage in male and female corpus

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

    #function implementation
    e1 = total_words_m_corpus * (wordcount_male + wordcount_female) / (total_words_m_corpus +
                                                                      total_words_f_corpus)
    e2 = total_words_m_corpus * (wordcount_male + wordcount_female) / (total_words_m_corpus
                                                                       +total_words_f_corpus)
    # print("e1 valaue: ", e1)
    # print("e2 value: ", e2)

    dunning_log_likelihood = 2 * (wordcount_male * math.log(wordcount_male / e1)) +2*(
        wordcount_female*math.log(wordcount_female/e2))

    # print(math.log10(wordcount_male / e1))  #WHY IS THIS VALUE ZERO??
    # print(math.log10(wordcount_female / e2))  #WHY IS THIS VALUE ZERO??


    if wordcount_male*math.log(wordcount_male/e1) < 0:
        dunning_log_likelihood = -dunning_log_likelihood

    #p = 1 - chi2.cdf(abs(dunning_log_likelihood),1)
    return dunning_log_likelihood

def dunning_total(m_corpus, f_corpus):
    '''
    goes through gendered corpora
    runs dunning_indiviidual on all words that are in BOTH corpora
    returns sorted dictionary of words and their dunning scores
    shows top 10 and lowest 10 words

    :return: dictionary of common word with dunning value and p value

         >>> c = Corpus('sample_novels')
         >>> m_corpus = c.filter_by_gender('male')
         >>> f_corpus = c.filter_by_gender('female')
         >>> dunning_total(m_corpus, f_corpus)
    '''
    wordcounter_male = m_corpus.get_wordcount_counter()
    wordcounter_female = f_corpus.get_wordcount_counter()

    totalmale_words = 0
    totalfemale_words = 0

    for male_word in wordcounter_male:
        totalmale_words += wordcounter_male[male_word]
    for female_word in wordcounter_female:
        totalfemale_words += wordcounter_female[female_word]

    dunning_result = {}
    for word in wordcounter_male:
        wordcount_male = wordcounter_male[word]
        if word in wordcounter_female:
            wordcount_female = wordcounter_female[word]
            dunning_result[word] = dunn_individual_word(totalmale_words,totalfemale_words,
                                                        wordcount_male,wordcount_female)
    dunning_result = sorted(dunning_result.items(), key = itemgetter(1))
    print(dunning_result)

    return dunning_result


import unittest

def instance_dist(novel, word):
    """
    >>> from gender_novels import novel
    >>> summary = "Hester was her convicted of adultery. "
    >>> summary += "which made her very sad, and then her Arthur was also sad, and her everybody was "
    >>> summary += "sad and then Arthur her died and it was very sad. her Sadness."
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1966',
    ...                   'filename': None, 'text': summary}
    >>> scarlett = novel.Novel(novel_metadata)
    >>> instance_dist(scarlett, "her")
    [6, 5, 6, 7, 7]

    :param:novel to analyze, gendered word
    :return: list of distances between instances of gendered word

    """
    output = []
    count = 0
    start = False
    text = novel.get_tokenized_text()

    for e in text:
        if not start:
            if e == word:
                start = True
        else:
            count += 1
            if e == word:
                output.append(count)
                count = 0
    return output



class Test(unittest.TestCase):
    def test_dunning_total(self):
        c = Corpus('sample_novels')
        m_corpus = c.filter_by_gender('male')
        f_corpus = c.filter_by_gender('female')
        results = dunning_total(m_corpus, f_corpus)
        print(results)

if __name__ == '__main__':
    unittest.main()

