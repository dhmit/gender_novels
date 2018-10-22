import math
from operator import itemgetter
from gender_novels.corpus import Corpus
from scipy.stats import chi2
import unittest



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

def dunning_total(counter1, counter2):
    '''
    runs dunning_individual on words shared by both counter objects
    (-) end of spectrum is words for counter_2
    (+) end of spectrum is words for counter_1
    the larger the magnitude of the number, the more distinctive that word is in its
    respective counter object

    :param:takes in two counter objects that map words to ints
    :return: dictionary of common words with dunning value, wordcount in corpus1, wordcount in corpus2

         >>> c = Corpus('sample_novels')
         >>> m_corpus = c.filter_by_gender('male')
         >>> f_corpus = c.filter_by_gender('female')
         >>> wordcounter_male = m_corpus.get_wordcount_counter()
         >>> wordcounter_female = f_corpus.get_wordcount_counter()
         >>> result = dunning_total(wordcounter_male, wordcounter_female)
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

            dunning_word = dunn_individual_word( total_words_counter1,  total_words_counter2,counter1_wordcount,counter2_wordcount)
            dunning_result[word] = (dunning_word, counter1_wordcount,counter2_wordcount)

    dunning_result = sorted(dunning_result.items(), key = itemgetter(1))
    print(dunning_result)

    return dunning_result


class Test(unittest.TestCase):
    def male_VS_female_analysis_dunning(self):
        '''
        tests word distinctiveness of shared words between male and female corpora using dunning
        :return: dictionary of coomon shared words and their distinctiveness
        '''
        c = Corpus('sample_novels')
        m_corpus = c.filter_by_gender('male')
        f_corpus = c.filter_by_gender('female')
        wordcounter_male = m_corpus.get_wordcount_counter()
        wordcounter_female = f_corpus.get_wordcount_counter()
        results = dunning_total(wordcounter_male, wordcounter_female)
        print(results[10::])
if __name__ == '__main__':
        unittest.main()

