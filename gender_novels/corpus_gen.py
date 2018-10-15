import csv
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata
from gutenberg.acquire import get_metadata_cache
import re
from pathlib import Path
import unittest
import pywikibot
import glob
from shutil import copyfile
import os
import gender_guesser.detector as gender_guesser

from gender_novels import common

# TODO: A lot of things

GUTENBERG_METADATA_PATH = common.GUTENBERG_METADATA_PATH
metadata_list = common.metadata_list
INITIAL_BOOK_STORE = common.INITIAL_BOOK_STORE # 30 books from gutenberg downloaded from Dropbox folder shared with Keith,
# plus some extras
FINAL_BOOK_STORE = common.FINAL_BOOK_STORE
SUBJECTS_TO_IGNORE = ["nonfiction", "dictionaries", "bibliography", "poetry", "short stories", "biography", "encyclopedias",
             "atlases", "maps", "words and phrase lists", "almanacs", "handbooks, manuals, etc.", "periodicals",
             "textbooks", "terms and phrases", "essays", "united states. constitution", "bible", "directories",
             "songbooks", "hymns", "correspondence", "drama", "reviews"] #is the Bible a novel?
AUTHOR_NAME_REGEX = common.AUTHOR_NAME_REGEX

def generate_corpus_gutenberg():
    """
    Generate metadata sheet of all novels we want from gutenberg
    >>> generate_corpus_gutenberg()
    """

    # determine current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print(current_dir)
    # write csv header
    with open(Path(current_dir, GUTENBERG_METADATA_PATH), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata_list)
        writer.writeheader()
    # check if cache is populated, if it isn't, populates it
    cache = get_metadata_cache()
    if (not cache.exists):
        cache.populate()
    # go through all books in Keith's thing
    bookshelf = str(Path(current_dir, INITIAL_BOOK_STORE, r"*.txt"))
    print(bookshelf)
    books = glob.iglob(bookshelf)
    for book in books:
        print(book)
        # get the book's id
        gutenberg_id = get_gutenberg_id(book)
        # check if book is valid novel by our definition
        if (not is_valid_novel_gutenberg(gutenberg_id, book)):
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
        write_metadata(novel_metadata, Path(current_dir, GUTENBERG_METADATA_PATH))
        # copy text file to new folder
        copyfile(book, Path(current_dir, FINAL_BOOK_STORE, str(gutenberg_id) + r".txt"))


def get_gutenberg_id(filepath):
    """
    For file with filepath get the gutenberg id of that book.  Should not be hard because gutenberg literally names
    files by id

    >>> from gender_novels import corpus_gen
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> get_gutenberg_id(Path(current_dir, r"corpora/test_books_30/44-0.txt"))
    44

    :param filepath: Path
    :return: int
    """
    filename = Path(filepath).name
    filename = filename.rstrip(r"-0.txt")
    return int(filename)

def is_valid_novel_gutenberg(gutenberg_id, filepath):
    """
    Determines whether book with this gutenberg id is actually a "novel".  Returns false if the book is not or doesn't
    actually exist.
    Should check:
    If book is English
    If book is under public domain
    If book is a "novel"
    if novel is in correct publication range
    That novel is not a translation

    >>> from gender_novels import corpus_gen
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> is_valid_novel_gutenberg(32, Path(current_dir, r"/corpora/test_books_30/32-0.txt")
    True
    >>> is_valid_novel_gutenberg(11000, Path(current_dir, r"corpora/test_books_30/11000-0.txt")
    False
    >>> is_valid_novel_gutenberg(1404, Path(current_dir, r"corpora/test_books_30/1404-0.txt")
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
        for word in SUBJECTS_TO_IGNORE:
            if ((subject.lower()).find(word) != -1):
                return False
    title = get_title_gutenberg(gutenberg_id)
    try:
        date = int(get_publication_date(get_author_gutenberg(gutenberg_id), title, gutenberg_id))
        if ((date < 1770 or date > 1922)):
            return False
    except TypeError:
        pass
    if (title.find("Index of the Project gutenberg ") != -1):
        return False
    if (title.find("Complete Project gutenberg ") != -1):
        return False
    text = get_novel_text_gutenberg(filepath)
    if (text.find("Translator: ", 0, 650) != -1):
        return False
    text_length = len(text)
    if (text_length < 140000 or text_length > 9609000 ): # Animal Farm is roughly 166700 characters including boilerplate
        # Guiness World Records states that the longest novel is 9,609,000 characters long
        return False
    return True

def get_author_gutenberg(gutenberg_id):
    """
    Gets author or authors for novel with this gutenberg id

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
    Gets title for novel with this gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_title_gutenberg(33)
    'The Scarlet Letter'

    """
    # TODO: run doctest on computer with populated cache

    return list(get_metadata('title', gutenberg_id))[0]

def get_novel_text_gutenberg(filepath):
    """
    Extract text as as string from file, with boilerplate removed

    >>> from gender_novels.corpus_gen import get_novel_text_gutenberg
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> book = get_novel_text_gutenberg(Path(current_dir, r"corpora/test_books_30/32-0.txt"))
    >>> book[:7]
    'HERLAND'

    :param gutenberg_id: int
    :return: str
    """
    if (common.get_encoding_type(filepath) != 'utf-8' or common.get_encoding_type(filepath) != 'UTF-8-SIG'):
        common.convertFileWithDetection(filepath)
        # converted_filepath = Path(Path(filepath).parent, r"converted", Path(filepath).name)
        # copyfile(converted_filepath, filepath)
    with open(filepath, mode='r', encoding='utf8') as text:
        text_with_headers = text.read()
        return strip_headers(text_with_headers).strip()


def get_publication_date(author, title, filepath, gutenberg_id = None):
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
    """
    #TODO: remember to uncomment worldcat function when it is done

    date = get_publication_date_from_copyright(get_novel_text_gutenberg(filepath))
    if (date != None):
        return date
    else:
        pass
        # date = get_publication_date_worldcat(author, title)
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
    # TODO: uncomment worldcat function once it is added
    country = None
    # country = get_country_publication_worldcat(author, title)
    if (country == None):
        country = get_country_publication_wikidata(author, title)
    return country

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
    # try to get publication country from wikidata page with title of book
    try:
        wikipedia = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(wikipedia, title)
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()
        clm_dict = dictionary["claims"]
        clm_list = clm_dict["P495"] # get claim "publication country", which is 495
        year = None
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            country_id = clm_trgt.id
    # in case of disambiguation
    except (KeyError):
        try:
            return get_country_publication_wikidata(author, title + " (novel)")
        except (pywikibot.exceptions.NoPage):
            return None
    except (pywikibot.exceptions.NoPage):
        return None

    # try to match country_id to major English-speaking countries
    if (country_id == "Q30"):
        return "United States"
    if (country_id == "Q145"):
        return "United Kingdom"
    if (country_id == "Q16"):
        return "Canada"
    if (country_id == "Q408"):
        return "Australia"
    if (country_id == "Q2886622"):
        return "Narnia" # I mean, they seem to all speak English there

    # if not try look up wikidata page of country with that id to try and get short name
    wikidata = pywikibot.Site("wikidata", "wikidata")
    repo = wikidata.data_repository()
    item = pywikibot.ItemPage(repo, country_id)
    dictionary = item.get()
    clm_dict = dictionary["claims"]
    clm_list = clm_dict["P1813"] # P1813 is short name
    for clm in clm_list:
        clm_trgt = clm.getTarget()
        if (clm_trgt.language == 'en'):
            return clm_trgt.text

    #if that doesn't work just get one of the aliases. Name may be awkwardly long but should be consistent
    country = dictionary['aliases']['en'][-1]
    return country

def get_author_gender(authors):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary', or 'both' (if there are multiple authors of different
    genders)
    #TODO: should get functions that fail to find anything return 'unknown'
    #TODO: 'both' is ambiguous; Does it mean both female and male?  female and unknown?  male and nonbinary?

    >>> from gender_novels.corpus_gen import get_author_gender
    >>> get_author_gender(["Hawthorne, Nathaniel"])
    'male'
    >>> get_author_gender(["Cuthbert, Michael"])
    'male'
    >>> get_author_gender(["Duan, Mingfei"])

    >>> get_author_gender(["Collins, Suzanne", "Riordan, Rick"])
    'both'
    >>> get_author_gender(["Shelley, Mary", "Austen, Jane"])
    'female'
    >>> get_author_gender(['Shakespeare, William', "Duan, Mingfei"])
    'both'

    :param authors: list
    :return: str
    """

    author_gender = None
    if type(authors) == str:
        authors = list().append(authors)
    if len(authors) == 1:
        author = authors[0]
        # author_gender = get_author_gender_worldcat(author)
        if author_gender == None:
            author_gender = get_author_gender_wikidata(author)
        if author_gender == None:
            guesser = gender_guesser.Detector()
            match = re.match(AUTHOR_NAME_REGEX, author)
            gender_guess = guesser.get_gender(match.groupdict()['first_name'])
            if (gender_guess == 'andy' or gender_guess == 'unknown'):
                author_gender = None
            if (gender_guess == 'male' or gender_guess == 'mostly male'):
                author_gender = 'male'
            if (gender_guess == 'female' or gender_guess == 'mostly female'):
                author_gender == 'female'
    else:
        author_gender = get_author_gender([authors[0]])
        for author in authors:
            if (get_author_gender([author]) != author_gender):
                author_gender = 'both'
    return author_gender

def get_author_gender_wikidata(author):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary' from wikidata
    If it fails returns 'unknown'
    N.B. Wikidata's categories for transgender male and female are treated as male and female, respectively

    >>> from gender_novels.corpus_gen import get_author_gender_wikidata
    >>> get_author_gender_wikidata("Obama, Barack")
    'male'
    >>> get_author_gender_wikidata("Hurston, Zora Neale")
    'female'
    >>> get_author_gender_wikidata("Bush, George W.")
    'male'

    :param author: str
    :return: str
    """

    match = re.match(AUTHOR_NAME_REGEX, author)
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
