import math
import numpy as np
from scipy import stats

from gender_novels.analysis import gender_pronoun_freq_analysis
from gender_novels.corpus import Corpus


def ind_ttest(array1, array2, pvalue_target=0.05):
    '''
    independent t-test for two independent variables
    :param array1: array-like, data for one category. e.g. he/she distance in novels authored by
    women
    :param array2: array-like, data for second category. e.g. he/she distance in novels authored
    by men
    :param pvalue_target: largest p-value for which we consider the test statistically significant
    :return: True if the difference in the means of the two arrays are significant, False otherwise
    >>> a1 = np.array([1, 2, 3, 4, 5])
    >>> a2 = np.array([1, 2, 3, 4, 5])
    >>> ind_ttest(a1, a2)
    False
    >>> a3 = np.array([3, 4, 8, 6, 2])
    >>> a4 = np.array([14, 8, 17, 9, 16])
    >>> ind_ttest(a3, a4)
    True
    '''

    # don't assume that the two variables have equal standard deviation
    pvalue = stats.ttest_ind(array1, array2, equal_var=False)[1]

    return pvalue < pvalue_target


def linear_regression(array1, array2, pvalue_target=0.05):
    '''
    linear regression on two continuous variables that may or may not be correlated
    :param array1: array-like, one set of continuous data to be compared to array2. e.g. list of
    publication years in a certain order of novels
    :param array2: array-like, second set of continuous data to be compared to array1, should be
    the same size as array1. e.g. he/she distance in the same order of novels as array1
    :param pvalue_target: largest p-value for which we consider the correlation statistically
    significant
    :return: True if the correlation is significant, False otherwise
    >>> a1 = np.array([1, 2, 3, 4, 5])
    >>> a2 = np.array([1, 2, 3, 4, 5])
    >>> linear_regression(a1, a2)
    True
    >>> a3 = np.array([3, 4, 8, 6, 2])
    >>> a4 = np.array([14, 8, 17, 9, 16])
    >>> linear_regression(a3, a4)
    False
    '''

    pvalue = stats.linregress(array1, array2)[3]
    return pvalue < pvalue_target


def pearson_correlation(array1, array2, pvalue_target=0.05):
    '''
    pearson correlation test of two continuous variables for correlation
    :param array1: array-like, one set of continuous data to be compared to array2
    :param array2: array-like, second set of continuous data to be compared to array1, should be
    the same size as array1
    :param pvalue_target: largest p-value for which we consider the correlation statistically
    significant
    :return: True if the correlation is significant, False otherwise
    >>> a1 = np.array([1, 2, 3, 4, 5])
    >>> a2 = np.array([1, 2, 3, 4, 5])
    >>> pearson_correlation(a1, a2)
    True
    >>> a3 = np.array([3, 4, 8, 6, 2])
    >>> a4 = np.array([14, 8, 17, 9, 16])
    >>> pearson_correlation(a3, a4)
    False
    '''

    pvalue = stats.pearsonr(array1, array2)[1]

    return pvalue < pvalue_target


if __name__ == "__main__":
    '''
    Finds the minimum p-value to deem the relationship between metadata variables and analysis 
    results significant
    
    Independent variables (metadata) include:
        author gender
        year of publication
        country of publication
    
    Dependent variables:
        distance between 'he' and 'she'
        the frequency of gendered pronouns used as subjects or objects
    '''

    corp = Corpus('test_corpus')
    # corp = Corpus('gutenberg')
    # corp = Corpus('sample_novels')
    subject_female_pronoun_dict = gender_pronoun_freq_analysis.subject_pronouns_gender_comparison(corp,
                                                                                              'female')
    # create lists for novels, publication date, etc. with all entries in the same
    # corresponding order
    novel_list = []
    novel_year_list = []
    novel_author_gender_list = []
    subject_female_pronoun_list = []

    for novel in corp:
        novel_list.append(novel)
        novel_year_list.append(novel.date)
        novel_author_gender_list.append(novel.author_gender)
        subject_female_pronoun_list.append(subject_female_pronoun_dict[novel])

    # split the subject_female_pronoun_list into a list for male authors and a list for female authors
    # used for independent t-test
    male_subject_pronoun_list = []
    female_subject_pronoun_list = []
    for novel in novel_list:
        if novel.author_gender == 'male':
            male_subject_pronoun_list.append(subject_female_pronoun_dict[novel])
        else:
            female_subject_pronoun_list.append(subject_female_pronoun_dict[novel])

    # test if the difference in frequency of female pronouns in novels authored by men vs by women is
    # significant
    # by iterating over p-values to find the minimum p-value
    print("Independent t-test on frequency of female pronouns as subjects in male-authored vs "
      "female-authored "
      "novels")
    for index in range(10):
        pvalue = (index+1)*0.05
        print("p-value target = " + str(round(pvalue, 2)) + ": " + str(ind_ttest(np.array(
        male_subject_pronoun_list), np.array(female_subject_pronoun_list),
                    pvalue)))

    # tests for the correlation between publication year and frequency of female pronouns as subjects
    print()
    print("Linear regression on publication year and frequency of female pronouns as subjects")
    for index in range(10):
        pvalue = (index+1)*0.05
        print("p-value target = " + str(round(pvalue, 2)) + ": " + str(linear_regression(np.array(
        novel_year_list), np.array(subject_female_pronoun_list), pvalue)))

    print()
    print("Pearson correlation on publication year and frequency of female pronouns as subjects")
    for index in range(10):
        pvalue = (index+1)*0.05
        print("p-value target = " + str(round(pvalue, 2)) + ": " + str(pearson_correlation(np.array(
        novel_year_list), np.array(subject_female_pronoun_list), pvalue)))
