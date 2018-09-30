"""
This file is intended for individual analyses of the gender_novels project

"""

from gender_novels.corpus import Corpus
from gender_novels.novel import Novel


def test_function():
    """
    TODO: Analysis team: please delete this function as soon as you write your own functions
    TODO: into this file--I only set it up so you'd have a place to start.

    :return:
    """

    corpus = Corpus('sample_novels')
    for novel in corpus.novels:
        count_she = novel.get_count_of_word('she')
        count_he = novel.get_count_of_word('he')
        print(f'{novel.author}: {novel.title}. Count she: {count_she}. Count he: {count_he}.')


if __name__ == '__main__':
    test_function()
