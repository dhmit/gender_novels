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

if __name__ == '__main__':
    test_function()


