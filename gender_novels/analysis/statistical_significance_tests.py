import math
import numpy as np
from scipy import stats

from gender_novels.analysis import gender_pronoun_freq_analysis
from gender_novels.corpus import Corpus


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html#scipy.stats.ttest_ind
def ind_ttest(array1, array2, pvalue_target=0.05):
    '''
    independent t test for two independent variables
    array1, array2: two array_like objects that represent data points for two categories
        for example, array1 could be he/she distance in novels authored by women, and array2 could containe he/she distance for novels authored by men
    pvalue_target: the largest p-value for which we consider the test statistic significant
    returns True if the difference in the means of the two datasets are statistically significant
    returns False if the difference in means can be explained by chance
    '''

    # don't assume that the two variables have equal standard deviation
    # pvalue = stats.ttest_ind(array1, array2, equal_var=False, nan_policy='omit')[1]
    pvalue = stats.ttest_ind(array1, array2, equal_var=False)[1]

    return pvalue < pvalue_target


# simple regression
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html#scipy.stats.linregress
def linear_regression(array1, array2, pvalue_target=0.05):
    pvalue = stats.linregress(array1, array2)[3]
    return pvalue < pvalue_target


# multiple regression

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html#scipy.stats.pearsonr
def pearson_correlation(array1, array2, pvalue_target=0.05):
    '''
    pearson correlation test of two continuous variables for correlation
    array1, array2: two array_like objects that represent data points for two continuous variables
    pvalue_target: the largest p-value for which we consider the correlation coefficient statistically significant
    returns True if there is a significant correlation
    returns False otherwise
    '''
    pvalue = stats.pearsonr(array1, array2)[1]

    return pvalue < pvalue_target


'''
independent variables:
    author gender
    year of publication
    character gender
    country of publication

dependent variables:
    distance between "he" and "she"
    subject vs object pronouns

use subject_pronouns_gender_comparison(corp, subject_gender)
'''

corp = Corpus('test_corpus')
# corp = Corpus('gutenberg')
# corp = Corpus('sample_novels')
subject_female_pronoun_dict = gender_pronoun_freq_analysis.subject_pronouns_gender_comparison(corp,
                                                                                              'female')

# create ordered list of novels
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
    print("p-value target = " + str(pvalue) + ": " + str(ind_ttest(np.array(
        male_subject_pronoun_list), np.array(female_subject_pronoun_list),
                    pvalue)))

print()
print("Linear regression on publication year and frequency of female pronouns as subjects")
for index in range(10):
    pvalue = (index+1)*0.05
    print("p-value target = " + str(pvalue) + ": " + str(linear_regression(np.array(
        novel_year_list), np.array(subject_female_pronoun_list), pvalue)))

print()
print("Pearson correlation on publication year and frequency of female pronouns as subjects")
for index in range(10):
    pvalue = (index+1)*0.05
    print("p-value target = " + str(pvalue) + ": " + str(pearson_correlation(np.array(
        novel_year_list), np.array(subject_female_pronoun_list), pvalue)))
