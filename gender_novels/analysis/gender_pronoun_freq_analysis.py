from gender_novels.corpus import Corpus
from gender_novels.analysis.analysis import get_comparative_word_freq
import numpy as np


def books_pronoun_freq(corp):
    '''
    Counts male and female pronouns for every book and finds their relatvie frequencies per book
    Outputs dictionary mapping novel object to the relative frequency of male pronouns in that book

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

    return (relative_freq_male)


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
    '''
    mean_dict = {}
    for k, v in data_dict.items():
        mean_dict[k] = np.mean(v)
    return mean_dict


if __name__ == "__main__":
    all_data = books_pronoun_freq(Corpus('sample_novels'))

    gender = freq_by_author_gender(all_data)
    date = freq_by_date(all_data)
    location = freq_by_location(all_data)

    print('By author gender: ')
    print(get_mean(gender))
    print('\n By date: ')
    print(get_mean(date))
    print('\n By location: ')
    print(get_mean(location))
