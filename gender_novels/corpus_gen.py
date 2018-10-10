import csv
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import re
import pywikibot
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
    #         title)
    #     novel_metadata['author_gender'] = get_author_gender(author)
    #     novel_metadata['subject'] = get_subject(author, title, id)
    #     # write to csv
    #     write_metadata(novel_metadata, GUTENBERG_METADATA_PATH)
    pass

def is_valid_novel_gutenberg(id):
    """
    Determines whether book with this Gutenberg id is actually an English
    language "novel".  Returns false if the book is not or doesn't actually
    exist.
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
    For a given novel id returns the full text of that novel from gutenberg as
    a string

    >>> from gender_novels import corpus_gen
    >>> scarlet_letter = get_novel_text_gutenberg(33)
    >>> scarlet_letter[:18]
    'THE SCARLET LETTER'

    :param novel_id: int
    :return: str
    """
    # TODO: implement this function
    text = strip_headers(load_etext(novel_id)).strip()
    return text

def get_publication_date(author, title, id = None):
    """
    For a given novel with id novel_id this function attempts a variety of
    methods to try and find the publication date
    If it can't returns None

    >>> from gender_novels import corpus_gen
    >>> get_publication_date("Hawthorne, Nathaniel", "The Scarlet Letter", 33)
    1850

    >>> from gender_novels import corpus_gen
    >>> get_publication_date("Dick, Phillip K.", "Mr. Spaceship", 32522)
    1953

    :param author: str
    :param title: str
    :param id: int
    :return: int
    TODO(duan): implement this function
    """
    #This function will call other get_publication_date functions in turn until a publication date is found
    pass

def get_publication_date_wikidata(author, title):
    """
    For a given novel with this author and title this function attempts to pull the publication year from Wikidata
    Otherwise returns None
    N.B.: This fails if the title is even slightly wrong (e.g. The Adventures of Huckleberry Finn vs Adventures of
    Huckleberry Finn).  Should it be tried to fix that?
    Function also doesn't use author parameter

    >>> from gender_novels import corpus_gen
    >>> get_publication_date_wikidata("Francis Bacon", "Novum Organum")
    1620
    >>> get_publication_date_wikidata("Mingfei Duan", "How I Became a Billionaire and also the President")

    >>> get_publication_date_wikidata("Jane Austen", "Persuasion")
    1818

    :param author: str
    :param title: str
    :return: int
    """

    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, title)
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()
        clm_dict = dictionary["claims"]
        clm_list = clm_dict["P577"]
        year = None
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            year = clm_trgt.year
    except (KeyError):
        try:
            return get_publication_date_wikidata(author, title + " (novel)")
        except (pywikibot.exceptions.NoPage):
            return None
    except (pywikibot.exceptions.NoPage):
        return None
    return year


def get_publication_date_from_copyright(novel_text):
    """
    Tries to extract the publication date from the copyright statement in the
    given text
    Otherwise returns None

    >>> novel_text = "This work blah blah blah blah COPYRIGHT, 1894 blah"
    >>> novel_text += "and they all died."
    >>> from gender_novels import corpus_gen
    >>> get_publication_date_from_copyright(novel_text)
    1894

    TODO: should this function take the novel's text as a string or the id or?
    TODO: should function also try to find publication years not prefaced with
        "copyright" at the risk of finding arbitrary 4-digit numbers?
    :param novel_text: string
    :return: int
    """
    match = re.search(r"(COPYRIGHT\,*\s*) (\d{4})", novel_text, flags = re.IGNORECASE)
    if (match == None):
        return None
    else:
        return int(match.group(2))

def get_country_publication(author, title):
    """
    Tries to get the country of novel
    @TODO: Country of origin or residence of author?

    >>> from gender_novels import corpus_gen
    >>> get_country_publication("Hawthorne, Nathaniel", "The Scarlet Letter")
    'United States'

    :param author: str
    :param title: str
    :return: str
    """
    # TODO(duan): implement this function
    pass

def get_author_gender(author):
    """
    Tries to get gender of author, 'female', 'male', or 'non-binary'.
    If it fails returns 'unknown'

    >>> from gender_novels import corpus_gen
    >>> get_author_gender("Hawthorne, Nathaniel")
    male

    :param author: str
    :return: str
    """
    # TODO(duan): implement this function
    pass

def get_subject(author, title, id = None):
    """
    Tries to get subjects
    TODO: Subject as defined by Gutenberg or LoC or what?
    :param: author: str
    :param: title: str
    :param: id: int
    :return: list
    """
    pass

def write_metadata(novel_metadata, path):
    """
    Writes a row of metadata for a novel into the csv at path
    :param: novel_metadata: dict
    :param: path: Path
    """
    pass

if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
