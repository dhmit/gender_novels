"""
This file is intended for individual analyses of the gender_novels project
"""

from gender_novels.corpus import Corpus
from gender_novels.novel import Novel

import numpy as np
import matplotlib.pyplot as plt


def test_function():
    d = {"Austin": [.5, .5], "Elliot": [.8, .2], "Sam": [.14, .22]}
    display_gender_freq(d=d, title="he_she_freq")  # made up data that works


def get_count_words(novel, words):
    """
        Returns the number of instances of each of elements of words in the text as a dictionary.  N.B.: Not case-sensitive.
        >>> from gender_novels import novel
        >>> summary = "Hester was convicted of adultery. "
        >>> summary += "which made her very sad, and then Arthur was also sad, and everybody was "
        >>> summary += "sad and then Arthur died and it was very sad.  Sadness."
        >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
        ...                   'corpus_name': 'sample_novels', 'date': 'long long ago',
        ...                   'filename': None, 'text': summary}
        >>> scarlett = novel.Novel(novel_metadata)
        >>> get_count_words(scarlett, ["sad", "and"])
        {"sad":4, "and":4}

        :param words: a list of words to be counted in text
        :return: a dictionary where the key is the word and the value is the count 
        """
    dic_word_counts = {}
    for word in words:
        dic_word_counts[word] = novel.get_count_of_word(word)
    return dic_word_counts

def get_comparative_word_freq(freqs):
    """
    Returns a dictionary of the frequency of words counted relative to each other

    :param freqs: dictionary
    :return: dictionary

    >>> from gender_novels import novel
    >>> novel_metadata = {'author': 'Hawthorne, Nathaniel', 'title': 'Scarlet Letter',
    ...                   'corpus_name': 'sample_novels', 'date': '1900',
    ...                   'filename': 'hawthorne_scarlet.txt'}
    >>> scarlet = novel.Novel(novel_metadata)
    >>> d = {'he':scarlet.get_word_freq('he'), 'she':scarlet.get_word_freq('she')}
    >>> d
    {'he': 0.00733, 'she': 0.00589}
    >>> x = get_comparative_word_freq(d)
    >>> x
    {'he': 0.55446, 'she': 0.44554}
    """

    total_freq = sum(freqs.values())
    comp_freqs = {}

    for k, v in freqs.items():
        freq = v / total_freq
        comp_freqs[k] = round(freq, 5)

    return comp_freqs


def display_gender_freq(d, title):
    """
    takes in a dictionary sorted by author and gender frequencies, and a title
    and outputs the resulting graph to 'visualizations/title.pdf' AND 'visualizations/title.png'
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

if __name__ == '__main__':
    test_function()


