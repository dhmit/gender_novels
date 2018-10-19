from gender_novels.corpus import Corpus
from gender_novels.analysis.analysis import get_comparative_word_freq
import numpy as np


def books_pronoun_freq(corp):
    #TODO: add doctests
    '''
    Counts male and female pronouns for every book and finds their relative frequencies per book
    Outputs dictionary mapping novel object to the relative frequency
        of female pronouns in that book

    :param: Corpus object
    :return: dictionary with data organized by groups
    '''

    relative_freq_male = {}
    relative_freq_female = {}

    for book in corp.novels:
        he = book.get_word_freq('he')
        him = book.get_word_freq('him')
        his = book.get_word_freq('his')
        male = he + him + his

        she = book.get_word_freq('she')
        her = book.get_word_freq('her')
        hers = book.get_word_freq('hers')
        female = she + her + hers

        temp_dict = {'male': male, 'female': female}
        temp_dict = get_comparative_word_freq(temp_dict)

        relative_freq_male[book] = temp_dict['male']
        relative_freq_female[book] = temp_dict['female']

    return (relative_freq_female)

def subject_vs_object_pronoun_freqs(corp):
    '''
    Takes in a Corpus of novels
    Returns a tuple of two dictionaries, one male and female
    Each dictionary maps each Novel in the corpus to the proportion of the pronouns
        of the specified gender in that novel that are subject pronouns

    #TODO: add doctests

    :param corp: Corpus
    :return: tuple of two dictionaries (male, female)
    '''

    relative_freq_male_subject = {}
    relative_freq_female_subject = {}
    relative_freq_male_object = {}
    relative_freq_female_object = {}

    for book in corp.novels:
        he = book.get_word_freq('he')
        him = book.get_word_freq('him')

        she = book.get_word_freq('she')
        her = book.get_word_freq('her')

        temp_dict_male = {'subject': he, 'object': him}
        temp_dict_female = {'subject': she, 'object': her}
        temp_dict_male = get_comparative_word_freq(temp_dict_male)
        temp_dict_female = get_comparative_word_freq(temp_dict_female)

        relative_freq_male_subject[book] = temp_dict_male['subject']
        relative_freq_female_subject[book] = temp_dict_female['subject']
        relative_freq_male_object[book] = temp_dict_male['object']
        relative_freq_female_object[book] = temp_dict_female['object']

        result_tuple = (relative_freq_male_subject, relative_freq_female_subject)

    return result_tuple

def subject_pronouns_gender_comparison(corp, subject_gender):
    '''
    Takes in a Corpus of novels and a gender.
    The gender determines whether the male frequency or female frequency will
        be returned
    Returns a dictionary of each novel in the Corpus mapped to the portion of
        the subject pronouns in the book that are of the specified gender
    :param corp: Corpus
    :param subject_gender: string 'male' or string 'female'
    :return: dictionary
    '''

    if not(subject_gender == 'male' or subject_gender == 'female'):
        raise ValueError('subject_gender must be \'male\' or \'female\'')

    relative_freq_female_sub = {}
    relative_freq_male_sub = {}

    for book in corp.novels:
        he = book.get_word_freq('he')
        she = book.get_word_freq('she')

        relative_freq_female_sub[book] = (she)/(he+she)
        relative_freq_male_sub[book] = (he)/(he+she)

    if subject_gender == 'male':
        return relative_freq_male_sub
    elif subject_gender == 'female':
        return relative_freq_female_sub
    else:
        raise ValueError('subject_gender must be \'male\' or \'female\'')

def dict_to_list(d):
    '''
    Takes in a dictionary and returns a list of the values in the dictionary
    If there are repeats in the values, there will be repeats in the list
    :param d: dictionary
    :return: list of values in the dictionary

    >>> d = {'a': 1, 'b': 'bee', 'c': 65}
    >>> dict_to_list(d)
    [1, 'bee', 65]

    >>> d2 = {}
    >>> dict_to_list(d2)
    []
    '''
    L = []
    for key, value in d.items():
        L.append(value)
    return L

def freq_by_author_gender(d):
    '''
    Takes in a dictionary of novel objects mapped to relative frequencies
        (output of above function)
    Returns a dictionary with frequencies binned by author gender into lists
        List name is mapped to the list of frequencies

    list names key:
    male_author - male authors
    female_author- female authors

    :param d: dictionary
    :return: dictionary

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Brontë, Anne', 'title': 'The Tenant of Wildfell Hall',
    ...                   'corpus_name': 'sample_novels', 'date': '1848', 'author_gender':'female',
    ...                   'filename': 'bronte_wildfell.txt'}
    >>> bronte = novel.Novel(novel_metadata)
    >>> novel_metadata = {'author': 'Adams, William Taylor', 'title': 'Fighting for the Right',
    ...                   'corpus_name': 'sample_novels', 'date': '1892', 'author_gender':'male',
    ...                   'filename': 'adams_fighting.txt'}
    >>> fighting = novel.Novel(novel_metadata)
    >>> d = {}
    >>> d[fighting] = 0.3
    >>> d[bronte] = 0.6
    >>> freq_by_author_gender(d)
    {'male_author': [0.3], 'female_author': [0.6]}
    '''

    male_author = []
    female_author = []
    data = {}

    for k, v in d.items():
        if k.author_gender == 'male':
            male_author.append(v)

        if k.author_gender == 'female':
            female_author.append(v)

    data['male_author'] = male_author
    data['female_author'] = female_author

    return data


def freq_by_date(d):
    '''
    Takes in a dictionary of novel objects mapped to relative frequencies
        (output of above function)
    Returns a dictionary with frequencies binned by decades into lists
        List name is mapped to the list of frequencies

    list names key:
    date_to_1810 - publication dates before and not including 1810
    date_x_to_y (by decade) - publication dates from x to y
        Example: date_1810_to_1819 - publication dates from 1810 to 1819
    date_1900_on - publication dates in 1900 and onward

    :param d: dictionary
    :return: dictionary

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
    ...                   'corpus_name': 'sample_novels', 'date': '1818',
    ...                   'filename': 'austen_persuasion.txt'}
    >>> austen = novel.Novel(novel_metadata)
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': 'hawthorne_scarlet.txt'}
    >>> scarlet = novel.Novel(novel_metadata)
    >>> d = {}
    >>> d[scarlet] = 0.5
    >>> d[austen] = 0.3
    >>> freq_by_date(d)
    {'date_to_1810': [], 'date_1810_to_1819': [0.3], 'date_1820_to_1829': [], 'date_1830_to_1839': [], 'date_1840_to_1849': [], 'date_1850_to_1859': [], 'date_1860_to_1869': [], 'date_1870_to_1879': [], 'date_1880_to_1889': [], 'date_1890_to_1899': [], 'date_1900_on': [0.5]}
    '''

    date_to_1810 = []
    date_1810_to_1819 = []
    date_1820_to_1829 = []
    date_1830_to_1839 = []
    date_1840_to_1849 = []
    date_1850_to_1859 = []
    date_1860_to_1869 = []
    date_1870_to_1879 = []
    date_1880_to_1889 = []
    date_1890_to_1899 = []
    date_1900_on = []

    data = {}

    for k, v in d.items():
        if k.date < 1810:
            date_to_1810.append(v)
        elif k.date < 1820:
            date_1810_to_1819.append(v)
        elif k.date < 1830:
            date_1820_to_1829.append(v)
        elif k.date < 1840:
            date_1830_to_1839.append(v)
        elif k.date < 1850:
            date_1840_to_1849.append(v)
        elif k.date < 1860:
            date_1850_to_1859.append(v)
        elif k.date < 1870:
            date_1860_to_1869.append(v)
        elif k.date < 1880:
            date_1870_to_1879.append(v)
        elif k.date < 1890:
            date_1880_to_1889.append(v)
        elif k.date < 1900:
            date_1890_to_1899
        else:
            date_1900_on.append(v)

    data['date_to_1810'] = date_to_1810
    data['date_1810_to_1819'] = date_1810_to_1819
    data['date_1820_to_1829'] = date_1820_to_1829
    data['date_1830_to_1839'] = date_1830_to_1839
    data['date_1840_to_1849'] = date_1840_to_1849
    data['date_1850_to_1859'] = date_1850_to_1859
    data['date_1860_to_1869'] = date_1860_to_1869
    data['date_1870_to_1879'] = date_1870_to_1879
    data['date_1880_to_1889'] = date_1880_to_1889
    data['date_1890_to_1899'] = date_1890_to_1899
    data['date_1900_on'] = date_1900_on

    return data


def freq_by_location(d):
    '''
    Takes in a dictionary of novel objects mapped to relative frequencies
        (output of above function)
    Returns a dictionary with frequencies binned by publication location into lists
        List name is mapped to the list of frequencies

    list names key:
    location_England - published in England
    location_US - published in the US
    location_other - published somewhere other than the US and England

    :param d: dictionary
    :return: dictionary

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
    ...                   'corpus_name': 'sample_novels', 'date': '1818',
    ...                   'country_publication': 'England', 'filename': 'austen_persuasion.txt'}
    >>> austen = novel.Novel(novel_metadata)
    >>> novel_metadata2 = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'country_publication': 'United States', 'filename':'hawthorne_scarlet.txt'}
    >>> scarlet = novel.Novel(novel_metadata2)
    >>> d = {}
    >>> d[scarlet] = 0.5
    >>> d[austen] = 0.3
    >>> freq_by_location(d)
    {'location_England': [0.3], 'location_US': [0.5], 'location_other': []}
    '''

    location_England = []
    location_US = []
    location_other = []

    for k, v in d.items():
        if k.country_publication == 'England':
            location_England.append(v)
        elif k.country_publication == 'United States':
            location_US.append(v)
        else:
            location_other.append(v)

    data = {}

    data['location_England'] = location_England
    data['location_US'] = location_US
    data['location_other'] = location_other

    return data


def get_mean(data_dict):
    '''
    Takes in a dictionary matching some object to lists and returns a dictionary of the
        original keys mapped to the mean of the lists

    :param data_dict: dictionary matching some object to lists
    :return: dictionary with original key mapped to an average of the input list

    >>> d = {}
    >>> d['fives'] = [5,5,5]
    >>> d['halfway'] = [0,1]
    >>> d['nothing'] = [0]
    >>> get_mean(d)
    {'fives': 5.0, 'halfway': 0.5, 'nothing': 0.0}
    '''
    mean_dict = {}
    for k, v in data_dict.items():
        mean_dict[k] = np.mean(v)
    return mean_dict

def sort_every_year(frequency_dict):
    '''
    Takes in a dictionary of novels mapped to pronoun frequencies and returns a dictionay of
        years mapped to lists of pronoun frequencies

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
    ...                   'corpus_name': 'sample_novels', 'date': '1818',
    ...                   'filename': 'austen_persuasion.txt'}
    >>> austen = novel.Novel(novel_metadata)
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': 'hawthorne_scarlet.txt'}
    >>> scarlet = novel.Novel(novel_metadata)
    >>> d = {}
    >>> d[scarlet] = 0.5
    >>> d[austen] = 0.3
    >>> sorted_years = sort_every_year(d)
    >>> print(sorted_years)
    {1900: [0.5], 1818: [0.3]}


    :param frequency_dict: dictionary of novels mapped to pronoun frequencies
    :return: dictionary of years mapped to lists of pronoun frequencies
    '''
    every_year_dict = {}
    for key,value in frequency_dict.items():
        frequency_list = [frequency_dict[key]]

        if key.date not in every_year_dict.keys():
            every_year_dict[key.date] = frequency_list

        elif key.date in every_year_dict.keys():
            every_year_dict[key.date].append(frequency_dict[key])

    return every_year_dict

  
if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
