import csv
import gutenberg
import re
from pathlib import Path
import unittest

from gender_novels import common
from gender_novels import novel

# TODO: A lot of things

def generate_corpus_gutenberg():
    """
    Generate metadata sheet of all novels we want from Gutenberg
    TODO: implement functions called here
    """
    # # go through all books in Gutenberg
    # for (id in range(58000)): #would be nice if we could check number of books
    #     # check if book is valid novel by our definition
    #     if (!is_valid_novel_gutenberg(id)):
    #         continue
    #     # begin compiling metadata.  Metadata not finalized
    #     novel_metadata = {'id': str(id), 'corpus': 'Gutenberg'}
    #     author = get_author_gutenberg(id)
    #     novel_metadata['author'] = author
    #     title = get_title_gutenberg(id)
    #     novel_metadata['title']
    #     novel_metadata['date'] = get_publication_date(author, title, id)
    #     # if book isn't published between 1700 and 1922, skip it
    #     if (novel_metadata['date'] < 1700 || novel_metadata['date'] > 1922):
    #         continue
    #     novel_metadata['country_publication'] = get_country_publication(author,
    #         title
    #     novel_metadata['author_gender'] = get_author_gender(author)
    #     novel_metadata['subject'] = get_subject(author, title, id)
    #     # write to csv
    #     write_metadata(novel_metadata)
    pass

def is_valid_novel_gutenberg(id):
    """
    Determines whether book with this Gutenberg id is actually an English
    language "novel"
    N.B. does not check if novel is in correct publication range

    >>> from gender_novels import corpus_gen
    >>> is_valid_novel_gutenberg(33)
    True

    >>> from gender_novels import corpus_gen
    >>> is_valid_novel_gutenberg(33420)
    False

    :param id: int
    :return: boolean
    TODO: determine what is a novel and implement this function
    """
    pass

def get_author_gutenberg(id):
    """
    Gets author for novel with this Gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_author_gutenberg(33)
    'Hawthorne, Nathaniel'

    :param id: int
    :return: str
    """
    # TODO: should we format author names like this?
    # TODO(duan): implement this function
    pass

def get_title_gutenberg(id):
    """
    Gets title for novel with this Gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_title_gutenberg(33)
    'The Scarlet Letter'

    TODO(duan): implement this function
    """
    pass

def get_novel_text_gutenberg(novel_id):
    """
    For a given novel id returns the full text of that novel from gutenberg as a string

    >>> from gender_novels import corpus_gen
    >>>

    :param novel_id: int
    :return: str
    """
    text = gutenberg.cleanup.strip_headers(gutenberg.acquire.load_etext(novel_id)).strip()
    return text

def get_publication_date(author, title, id = None):
    """
    For a given novel with id novel_id this function attempts a variety of methods to try and
    find the publication date
    :param author: str
    :param title: str
    :param id: int
    :return: int
    TODO(duan): implement this function
    """
    pass

def get_publication_date_from_copyright(novel_text):
    """
    Tries to extract the publication date from the copyright statement in the given text
    >>> novel_text = "This work blah blah blah blah COPYRIGHT, 1894 blah
    >>> novel_text += and they all died."
    >>> from gender_novels import corpus_gen
    >>> get_publication_date_from_copyright(novel_text)
    1894

    TODO: should this function take the novel's text as a string or the id or?
    TODO: should function also try to find publication years not prefaced with "copyright" at
        the risk of finding arbitrary 4-digit numbers?
    :param novel_text: string
    :return: int
    """
    match = re.search(r"(COPYRIGHT\,*\s*) (\d{4})", novel_text, flags = re.IGNORECASE)
    return match.group(2)

if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
