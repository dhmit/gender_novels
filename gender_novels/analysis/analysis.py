"""
This file is intended for individual analyses of the gender_novels project

"""

from gender_novels.corpus import Corpus
from gender_novels.novel import Novel

import numpy as np
import matplotlib.pyplot as plt


def test_function():
    """
    TODO: Analysis team: please delete this function as soon as you write your own functions
    TODO: into this file--I only set it up so you'd have a place to start.

    :return:
    """
    '''
    corpus = Corpus('sample_novels')
    for novel in corpus.novels:
        count_she = novel.get_count_of_word('she')
        count_he = novel.get_count_of_word('he')
        print(f'{novel.author}: {novel.title}. Count she: {count_she}. Count he: {count_he}.')
    '''
    d = {"Austin": [.5, .5], "Elliot": [.8, .2], "Sam": [.14, .22]}
    display_gender_data(d)  # made up data that works


def display_gender_data(d):
    """
    takes in a dictionary sorted by author and gender frequencies
                and returns a graph visualization
                dictionary format {"Author/Novel": [he_freq, she_freq]}

                Will scale to allow inputs of larger dictionaries with non-binary values

                :param d:
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
    plt.show()
    return


if __name__ == '__main__':
    test_function()


