import csv
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.acquire import get_metadata_cache
import re
from pathlib import Path
import unittest
import pywikibot

from gender_novels import common

# TODO: A lot of things

GUTENBERG_MIRROR_PATH = ''
GUTENBERG_METADATA_PATH = Path('corpora', 'gutenberg', 'gutenberg.csv')
metadata_list = ['gutenberg_id', 'author', 'date', 'title', 'country_publication', 'author_gender', 'subject', 'corpus_name',
                 'notes']

def generate_corpus_gutenberg():
    """
    Generates folder with all UTF-8 .txt files of all valid novels.  Only works on Keith's computer.
    """
    # TODO (Keith): implement this function
    pass

def generate_corpus_metadata_gutenberg():
    """
    Generate metadata sheet of all novels we want from Gutenberg
    TODO: implement functions called here
    """
    # TODO: make this work with new system

    # function currently will not work
    pass

    # write csv header
    with open(GUTENBERG_METADATA_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata_list)
        writer.writeheader()
    # check if cache is populated, if it isn't, populates it
    cache = get_metadata_cache()
    if (not cache.exists()):
        cache.populate()
    # go through all books in Gutenberg
    for gutenberg_id in range(gutenberg_number_of_books()): # would be nice if we could check number of books
        # check if book is valid novel by our definition
        if (not is_valid_novel_gutenberg(gutenberg_id)):
            continue
        # begin compiling metadata.  Metadata not finalized
        novel_metadata = {'gutenberg_id': gutenberg_id, 'corpus_name': 'gutenberg'}
        author = get_author_gutenberg(gutenberg_id)
        novel_metadata['author'] = author
        title = get_title_gutenberg(gutenberg_id)
        novel_metadata['title'] = title
        novel_metadata['date'] = get_publication_date(author, title, gutenberg_id)
        # if book isn't published between 1700 and 1922, skip it
        if (novel_metadata['date'] < 1700 or novel_metadata['date'] > 1922):
            continue
        novel_metadata['country_publication'] = get_country_publication(author,
            title)
        novel_metadata['author_gender'] = get_author_gender(author)
        novel_metadata['subject'] = get_subject_gutenberg(gutenberg_id)
        # write to csv
        write_metadata(novel_metadata, GUTENBERG_METADATA_PATH)

def gutenberg_number_of_books():
    """
    Determines how many books currently exist in our Gutenberg mirror
    :return: int
    """
    # TODO: implement this function and make it return a legit count
    return 60000

def is_valid_novel_gutenberg(gutenberg_id):
    """
    Determines whether book with this Gutenberg id is actually a"novel".  Returns false if the book is not or doesn't
    actually exist.
    Should check:
    If book with this id exists
    If book is under public domain
    If book is a "novel"
    N.B. does not check if novel is in correct publication range

    >>> from gender_novels import corpus_gen
    >>> is_valid_novel_gutenberg(33)
    True

    >>> from gender_novels import corpus_gen
    >>> is_valid_novel_gutenberg(33420)
    False

    :param gutenberg_id: int
    :return: boolean
    TODO: determine what is a novel and implement this function
    """
    pass

def get_author_gutenberg(gutenberg_id):
    """
    Gets author or authors for novel with this Gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_author_gutenberg(33)
    ['Hawthorne, Nathaniel']

    :param gutenberg_id: int
    :return: list
    """
    # TODO: should we format author names like this?
    # TODO: possibly have this return a list of authors, rather than a single string, to handle multiple authors
    # TODO: run doctest on computer with populated cache

    return list(get_metadata('author', gutenberg_id))

def get_title_gutenberg(gutenberg_id):
    """
    Gets title for novel with this Gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_title_gutenberg(33)
    'The Scarlet Letter'

    """
    # TODO: run doctest on computer with populated cache

    return list(get_metadata('title', gutenberg_id))[0]

def get_novel_text_gutenberg(gutenberg_id):
    """
    For a given novel id returns the full text of that novel from gutenberg as
    a string

    >>> from gender_novels import corpus_gen
    >>> scarlet_letter = get_novel_text_gutenberg(33)
    >>> scarlet_letter[:18]
    'THE SCARLET LETTER'

    :param gutenberg_id: int
    :return: str
    """
    # TODO: make this work with new system
    # text = strip_headers(load_etext(gutenberg_id, mirror=GUTENBERG_MIRROR_PATH)).strip()
    # return text

def get_publication_date(author, title, gutenberg_id = None):
    """
    For a given novel with id gutenberg_id this function attempts a variety of
    methods to try and find the publication date
    If it can't returns None

    >>> from gender_novels import corpus_gen
    >>> get_publication_date("Hawthorne, Nathaniel", "The Scarlet Letter", 33)
    1850

    >>> from gender_novels import corpus_gen
    >>> get_publication_date("Dick, Phillip K.", "Mr. Spaceship", 32522)
    1953

    :param author: list
    :param title: str
    :param gutenberg_id: int
    :return: int
    TODO: implement this function
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
    >>> get_publication_date_wikidata("Bacon, Francis", "Novum Organum")
    1620
    >>> get_publication_date_wikidata("Duan, Mingfei", "How I Became a Billionaire and also the President")

    >>> get_publication_date_wikidata("Austen, Jane", "Persuasion")
    1818

    :param author: list
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
    USA should be written as United States
    Separate countries of UK (England, Wales, etc.)
    TODO: should we separate those countries?  Easier to integrate later than separate

    >>> from gender_novels import corpus_gen
    >>> get_country_publication("Hawthorne, Nathaniel", "The Scarlet Letter")
    'United States'

    :param author: list
    :param title: str
    :return: str
    """
    # TODO(duan): implement this function
    pass

def get_country_publication_wikidata(author, title):
    """
    Tries to get country of origin of author from wikidata
    Otherwise, returns None
    # TODO: see get_country_publication

    >>> from gender_novels import corpus_gen
    >>> get_country_publication_wikidata("Trump, Donald", "Trump: The Art of the Deal")
    'United States'

    :param author: list
    :param title: str
    :return: str
    """
    # TODO: implement this function
    pass

def get_author_gender(author):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary', or 'both' (if there are multiple authors of different
    genders)
    If it fails returns 'unknown'

    >>> from gender_novels import corpus_gen
    >>> get_author_gender("Hawthorne, Nathaniel")
    male

    :param author: list
    :return: str
    """
    # TODO: implement this function
    pass

def get_author_gender_wikidata(author):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary' from wikidata
    If it fails returns 'unknown'
    N.B. Wikidata's categories for transgender male and female are treated as male and female, respectively

    >>> from gender_novels import corpus_gen
    >>> get_author_gender_wikidata("Obama, Barack")
    'male'
    >>> get_author_gender_wikidata("Hurston, Zora Neale")
    'female'

    :param author: str
    :return: str
    """

    match = re.match(r"(?P<last_name>(\w+ )*\w*)\, (?P<first_name>(\w+ )*\w*)", author)
    author_formatted = match.groupdict()['first_name'] + " " + match.groupdict()['last_name']
    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, author_formatted)
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()
        clm_dict = dictionary["claims"]
        clm_list = clm_dict["P21"]
        gender_id = None
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            gender_id = clm_trgt.id
        if (gender_id == 'Q6581097' or gender_id == 'Q2449503'):
            return 'male'
        if (gender_id == 'Q6581072'or gender_id == 'Q1052281'):
            return 'female'
        if (gender_id == 'Q1097630'):
            return 'non-binary'
    except (KeyError, pywikibot.exceptions.NoPage):
        return None

def get_subject_gutenberg(gutenberg_id):
    """
    Tries to get subjects

    >>> from gender_novels import corpus_gen
    >>> get_subject_gutenberg(5200)

    :param: author: str
    :param: title: str
    :param: id: int
    :return: list
    """
    # TODO: run doctest on computer with populated cache

    return sorted(list(get_metadata('subject', gutenberg_id)))

def write_metadata(novel_metadata):
    """
    Writes a row of metadata for a novel into the csv at path
    Subject to change as metadata changes

    Running this doctest actually generates a file
    # >>> from gender_novels import corpus_gen
    # >>> corpus_gen.write_metadata({'id': 105, 'author': 'Austen, Jane', 'title': 'Persuasion',
    # ...                            'corpus_name': 'gutenberg', 'date': '1818',
    # ...                            'country_publication': 'England', 'subject': ['England -- Social life and customs -- 19th century -- Fiction'],
    # ...                            'author_gender': 'female'})

    :param: novel_metadata: dict
    :param: path: Path
    """
    corpus = novel_metadata['corpus_name']
    path = Path('corpora', corpus, f'{corpus}.csv')
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata_list)
        writer.writerow(novel_metadata)

if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
