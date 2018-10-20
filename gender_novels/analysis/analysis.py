"""
This file is intended for individual analyses of the gender_novels project
"""

from gender_novels.corpus import Corpus
import nltk
import math
from operator import itemgetter
nltk.download('stopwords', quiet=True)
# TODO: add prior two lines to setup, necessary to run
import collections
from scipy.stats import chi2
from statistics import mean, median, mode
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.palplot(sns.color_palette(palette="pastel"))


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
                sorted_words[tag].update({word: freqs[word]})
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
    plt.ylim(0, 1)

    index = np.arange(len(d.keys()))
    bar_width = 0.35

    he_val = tuple(he_val)
    she_val = tuple(she_val)
    authors = tuple(authors)

    rects1 = ax.bar(index, he_val, bar_width, color='cyan', label='He')

    rects2 = ax.bar(index + bar_width, she_val, bar_width, color='plum', label='She')

    ax.set_xlabel('Authors')
    ax.set_ylabel('Frequency')
    ax.set_title('Gendered Pronouns by Author')
    ax.set_xticks(index + bar_width / 2)
    plt.xticks(fontsize=8, rotation=90)
    ax.set_xticklabels(authors)
    ax.legend()

    fig.tight_layout()
    filepng = "visualizations/he_she_freq" + title + ".png"
    filepdf = "visualizations/he_she_freq" + title + ".pdf"
    plt.savefig(filepng, bbox_inches='tight')
    plt.savefig(filepdf, bbox_inches='tight')


def run_gender_freq(corpus):
    """
    Runs a program that uses the gender frequency analysis on all novels existing in a given
    corpus, and outputs the data as graphs
    :param corpus:
    :return:
    """
    novels = corpus._load_novels()
    c = len(novels)
    loops = c//10 + 1

    num = 0

    while num < loops:
        dictionary = {}
        for novel in novels[num * 10: min(c, num * 10 + 9)]:
            d = {'he': novel.get_word_freq('he'), 'she': novel.get_word_freq('she')}
            d = get_comparative_word_freq(d)
            lst = [d["he"], d["she"]]
            book = novel.title[0:20] + "\n" + novel.author
            dictionary[book] = lst
        display_gender_freq(dictionary, str(num))
        num += 1


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


def process_medians(helst, shelst, authlst):
    """
    >>> medians_he = [12, 130, 0, 12, 314, 18, 15, 12, 123]
    >>> medians_she = [123, 52, 12, 345, 0,  13, 214, 12, 23]
    >>> books = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    >>> process_medians(helst=medians_he, shelst=medians_she, authlst=books)
    {'he': [0, 2.5, 0, 1.3846153846153846, 0, 1.0, 5.3478260869565215], 'she': [10.25, 0, 28.75,
    0, 14.266666666666667, 0, 0], 'book': ['a', 'b', 'd', 'f', 'g', 'h', 'i']}

    :param helst:
    :param shelst:
    :param authlst:
    :return: a dictionary sorted as so {
                                        "he":[ratio of he to she if >= 1, else 0],
                                        "she":[ratio of she to he if > 1, else 0]
                                        "book":[lst of book authors]
                                       }
    """
    d = {"he": [], "she": [], "book": []}
    for num in range(len(helst)):
        if helst[num] > 0 and shelst[num] > 0:
            res = helst[num] - shelst[num]
            if res >= 0:
                d["he"].append(helst[num] / shelst[num])
                d["she"].append(0)
                d["book"].append(authlst[num])
            else:
                d["he"].append(0)
                d["she"].append(shelst[num] / helst[num])
                d["book"].append(authlst[num])
        else:
            if helst == 0:
                print("ERR: no MALE values: " + authlst[num])
            if shelst == 0:
                print("ERR: no FEMALE values: " + authlst[num])
    return d


def bubble_sort_across_lists(dictionary):
    """
    >>> d = {'he': [0, 2.5, 0, 1.3846153846153846, 0, 1.0, 5.3478260869565215],
    ...     'she': [10.25, 0, 28.75, 0, 14.266666666666667, 0, 0],
    ...     'book': ['a', 'b', 'd', 'f', 'g', 'h', 'i']}
    >>> bubble_sort_across_lists(d)
    {'he': [5.3478260869565215, 2.5, 1.3846153846153846, 1.0, 0, 0, 0], 'she': [0, 0, 0, 0,
    10.25, 14.266666666666667, 28.75], 'book': ['i', 'b', 'f', 'h', 'a', 'g', 'd']}

    :param dictionary: containing 3 different list values.
    Note: dictionary keys MUST contain arguments 'he', 'she', and 'book'
    :return dictionary sorted across all three lists in a specific method:
    1) Descending order of 'he' values
    2) Ascending order of 'she' values
    3) Corresponding values of 'book' values
    """
    lst1 = dictionary['he']
    lst2 = dictionary['she']
    lst3 = dictionary['book']
    r = range(len(lst1) - 1)
    p = True

    # sort by lst1 descending
    for j in r:
        for i in r:
            if lst1[i] < lst1[i + 1]:
                # manipulating lst 1
                temp1 = lst1[i]
                lst1[i] = lst1[i + 1]
                lst1[i + 1] = temp1
                # manipulating lst 2
                temp2 = lst2[i]
                lst2[i] = lst2[i + 1]
                lst2[i + 1] = temp2
                # manipulating lst of authors
                temp3 = lst3[i]
                lst3[i] = lst3[i + 1]
                lst3[i + 1] = temp3
                p = False
        if p:
            break
        else:
            p = True

    # sort by lst2 ascending
    for j in r:
        for i in r:
            if lst2[i] > lst2[i + 1]:
                # manipulating lst 1
                temp1 = lst1[i]
                lst1[i] = lst1[i + 1]
                lst1[i + 1] = temp1
                # manipulating lst 2
                temp2 = lst2[i]
                lst2[i] = lst2[i + 1]
                lst2[i + 1] = temp2
                # manipulating lst of authors
                temp3 = lst3[i]
                lst3[i] = lst3[i + 1]
                lst3[i + 1] = temp3
                p = False
        if p:
            break
        else:
            p = True
    d = {}
    d['he'] = lst1
    d['she'] = lst2
    d['book'] = lst3
    return d


def instance_stats(book, medians1, medians2, title):
    """
    :param book:
    :param medians1:
    :param medians2:
    :param title:
    :return: file written to visualizations folder depicting the ratio of two values given as a
    bar graph
    """
    fig, ax = plt.subplots()
    plt.ylim(0, 1000)

    index = np.arange(len(book))
    bar_width = .7

    medians_she = tuple(medians2)
    medians_he = tuple(medians1)
    book = tuple(book)

    rects1 = ax.bar(index, medians_he, bar_width, color='cyan', label='Male to Female')

    rects2 = ax.bar(index, medians_she, bar_width, color='plum', label='Female to Male')

    ax.set_xlabel('Book')
    ax.set_ylabel('Ratio of Median Values')
    ax.set_title(
        'MtF or FtM Ratio of Median Distance of Gendered Instances by Author')
    ax.set_xticks(index)
    plt.xticks(fontsize=8, rotation=90)
    ax.set_xticklabels(book)
    ax.set_yscale("symlog")

    ax.legend()

    fig.tight_layout()
    filepng = "visualizations/" + title + ".png"
    filepdf = "visualizations/" + title + ".pdf"
    plt.savefig(filepng, bbox_inches='tight')
    plt.savefig(filepdf, bbox_inches='tight')


def run_dist_inst(corpus):
    """
    Runs a program that uses the instance distance analysis on all novels existing in a given
    corpus, and outputs the data as graphs
    :param corpus:
    :return:
    """
    novels = corpus._load_novels()
    c = len(novels)
    loops = c//10 + 1

    num = 0

    while num < loops:
        medians_he = []
        medians_she = []
        books = []
        for novel in novels[num * 10: min(c, num * 10 + 9)]:
            result_he = instance_dist(novel, "he")
            result_she = instance_dist(novel, "she")
            try:
                medians_he.append(median(result_he))
            except:
                medians_he.append(0)
            try:
                medians_she.append(median(result_she))
            except:
                medians_she.append(0)
            books.append(novel.title[0:20] + "\n" + novel.author)
        d = process_medians(helst=medians_he, shelst=medians_she, authlst=books)
        d = bubble_sort_across_lists(d)
        instance_stats(d["book"], d["he"], d["she"], "inst_dist" + str(num))
        num += 1


class Test(unittest.TestCase):
    def test_dunning_total(self):
        c = Corpus('sample_novels')
        m_corpus = c.filter_by_gender('male')
        f_corpus = c.filter_by_gender('female')
        results = dunning_total(m_corpus, f_corpus)
        print(results)


if __name__ == '__main__':
    # unittest.main()
    run_dist_inst(Corpus('sample_novels'))
    # run_gender_freq(Corpus('sample_novels'))

