import csv
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
from gutenberg.acquire import get_metadata_cache
import re
from pathlib import Path
import unittest
import pywikibot
import glob
from shutil import copyfile

from gender_novels import common

# TODO: A lot of things

GUTENBERG_MIRROR_PATH = ''
GUTENBERG_METADATA_PATH = Path('corpora', 'gutenberg', 'gutenberg.csv')
metadata_list = ['gutenberg_id', 'author', 'date', 'title', 'country_publication', 'author_gender', 'subject', 'corpus_name',
                 'notes']
INITIAL_BOOK_STORE = r'/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30'
FINAL_BOOK_STORE = r'/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_corpus'

BAD_WORDS = ["nonfiction", "dictionaries", "bibliography", "poetry", "short stories", "biography", "encyclopedias",
             "atlases", "maps", "words and phrase lists", "almanacs", "handbooks, manuals, etc.", "periodicals",
             "textbooks", "terms and phrases", "essays", "united states. constitution", "bible", "directories",
             "songbooks", "hymns", "correspondence", "drama", "reviews"] #is the Bible a novel?

def generate_corpus_gutenberg():
    """
    Generate metadata sheet of all novels we want from Gutenberg
    TODO: implement functions called here
    """
    # TODO(duan): make this work with new system

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
    # go through all books in Keith's thing
    books = glob.iglob(INITIAL_BOOK_STORE+r"/*.txt")
    for book in books:
        # get the book's id
        gutenberg_id = get_gutenberg_id(book)
        # check if book is valid novel by our definition
        if (not is_valid_novel_gutenberg(gutenberg_id)):
            continue
        # begin compiling metadata.  Metadata not finalized
        novel_metadata = {'gutenberg_id': gutenberg_id, 'corpus_name': 'gutenberg'}
        author = get_author_gutenberg(gutenberg_id)
        novel_metadata['author'] = author
        title = get_title_gutenberg(gutenberg_id)
        novel_metadata['title'] = title
        novel_metadata['date'] = get_publication_date(author, title, gutenberg_id, book)
        novel_metadata['country_publication'] = get_country_publication(author,
            title)
        novel_metadata['author_gender'] = get_author_gender(author)
        novel_metadata['subject'] = get_subject_gutenberg(gutenberg_id)
        # write to csv
        write_metadata(novel_metadata, GUTENBERG_METADATA_PATH)
        # copy text file to new folder
        copyfile(book, FINAL_BOOK_STORE + r"/" + str(gutenberg_id) + r".txt")

def get_gutenberg_id(filepath):
    """
    For file with filepath get the gutenberg id of that book.  Should not be hard because Gutenberg literally names
    files by id

    >>> from gender_novels import corpus_gen
    >>> get_gutenberg_id(r"/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30/44-0.txt")
    44

    :param filepath: str
    :return: int
    """
    # TODO(duan): implement this function
    filepath = filepath.rstrip(r"-0.txt")
    filepath = filepath.lstrip(INITIAL_BOOK_STORE + r"/")
    return int(filepath)

def is_valid_novel_gutenberg(gutenberg_id, filepath):
    """
    Determines whether book with this Gutenberg id is actually a "novel".  Returns false if the book is not or doesn't
    actually exist.
    Should check:
    If book is English
    If book is under public domain
    If book is a "novel"
    if novel is in correct publication range

    >>> from gender_novels import corpus_gen
    >>> is_valid_novel_gutenberg(32, r"/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30/32-0.txt")
    True
    >>> is_valid_novel_gutenberg(11000, r"/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30/11000-0.txt")
    False
    >>> is_valid_novel_gutenberg(1404, r"/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30/1404-0.txt")
    False

    :param gutenberg_id: int
    :return: boolean
    TODO: increase selectivity (apparently The Federalist Papers is a novel)
    """
    language = list(get_metadata('language', gutenberg_id))[0]
    if (not language == 'en'):
        return False
    rights = get_metadata('rights', gutenberg_id)
    if (not rights == frozenset({'Public domain in the USA.'})):
        return False
    subjects = get_subject_gutenberg(gutenberg_id)
    for subject in subjects:
        for word in BAD_WORDS:
            if ((subject.lower()).find(word) != -1):
                return False
    title = get_title_gutenberg(gutenberg_id)
    try:
        date = int(get_publication_date(get_author_gutenberg(gutenberg_id), title, gutenberg_id))
        if ((date < 1770 or date > 1922)):
            return False
    except TypeError:
        pass
    if (title.find("Index of the Project Gutenberg ") != -1):
        return False
    if (title.find("Complete Project Gutenberg ") != -1):
        return False
    text_length = len(get_novel_text_gutenberg(filepath))
    if (text_length < 140000 or text_length > 9609000 ): # Animal Farm is roughly 166700 characters including boilerplate
        # Guiness World Records states that the longest novel is 9,609,000 characters long
        return False
    return True

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

def get_novel_text_gutenberg(filepath):
    """
    Extract text as as string from file, with boilerplate removed

    >>> from gender_novels import corpus_gen
    >>> book = get_novel_text_gutenberg(r"/home/fsae/mingfei_temp/gender_novels/gender_novels/corpora/test_books_30/32-0.txt")
    >>> book[:7]
    'HERLAND'

    :param gutenberg_id: int
    :return: str
    """
    # TODO(duan): make this work with new system
    with open(filepath, 'r') as text:
        return strip_headers(text.read()).strip()

def get_publication_date(author, title, gutenberg_id = None, filepath):
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
    TODO: will not work without worldcat functions
    """
    date = get_publication_date_from_copyright(get_novel_text_gutenberg(filepath))
    if (date != None):
        return date
    else:
        date = get_publication_date_worldcat(author, title)
    if (date != None):
        return date
    else:
        return get_publication_date_wikidata(author, title)

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
    Don't separate countries of UK (England, Wales, etc.)
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
    Tries to get country of publication from wikidata
    Otherwise, returns None
    >>> from gender_novels import corpus_gen
    >>> get_country_publication_wikidata("Trump, Donald", "Trump: The Art of the Deal")
    'United States'

    :param author: list
    :param title: str
    :return: str
    """
    # TODO(duan): implement this function
    try:
        wp = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(wp, title)
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()
        clm_dict = dictionary["claims"]
        clm_list = clm_dict["P495"]
        year = None
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            country_id = clm_trgt.id
    except (KeyError):
        try:
            return get_country_publication_wikidata(author, title + " (novel)")
        except (pywikibot.exceptions.NoPage):
            return None
    except (pywikibot.exceptions.NoPage):
        return None
    if (country_id == "Q30"):
        return "United States"
    if (country_id == "Q145"):
        return "United Kingdom"
    country = None
    wikidata = pywikibot.Site("wikidata", "wikidata")
    repo = wikidata.data_repository()
    item = pywikibot.ItemPage(repo, country_id)
    dictionary = item.get()
    clm_dict = dictionary["claims"]
    clm_list = clm_dict["P1813"]
    for clm in clm_list:
        clm_trgt = clm.getTarget()
        if (clm_trgt.language == 'en'):
            country = clm_trgt.text
    if (country == None):
        country = dictionary['aliases']['en'][-1]
    return country

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
