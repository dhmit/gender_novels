import csv
import glob
import os
import re
import time
from pathlib import Path
from shutil import copyfile

import gender_guesser.detector as gender_guesser
import pywikibot
from gutenberg.acquire import get_metadata_cache
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_metadata

from gender_novels import common
from gender_novels.common import GUTENBERG_METADATA_PATH, INITIAL_BOOK_STORE, FINAL_BOOK_STORE, \
    AUTHOR_NAME_REGEX, METADATA_LIST

# TODO: A lot of things

SUBJECTS_TO_IGNORE = ["nonfiction", "dictionaries", "bibliography", "poetry", "short stories", "biography", "encyclopedias",
             "atlases", "maps", "words and phrase lists", "almanacs", "handbooks, manuals, etc.", "periodicals",
             "textbooks", "terms and phrases", "essays", "united states. constitution", "bible", "directories",
             "songbooks", "hymns", "correspondence", "drama", "reviews", "translations into english", 'religion']
TRUNCATORS = ["\r", "\n", r"; Or, "]
COUNTRY_ID_TO_NAME = {"Q30":  "United States", "Q145": "United Kingdom", "Q21": "United Kingdom", "Q16": "Canada",
                      "Q408": "Australia", "Q2886622": "Narnia"}

def generate_corpus_gutenberg():
    """
    Generate metadata sheet of all novels we want from gutenberg
    >>> generate_corpus_gutenberg()
    """

    # determine current directory
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print("Current directory:",current_dir)
    # write csv header
    with open(Path(current_dir, GUTENBERG_METADATA_PATH), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=METADATA_LIST)
        writer.writeheader()
        print("Wrote metadata header")
    # check if cache is populated, if it isn't, populates it
    cache = get_metadata_cache()
    if (not cache.exists):
        print("Populating cache...")
        cache.populate()
        print("Done populating cache")
    # go through all books in Keith's thing
    bookshelf = str(Path(current_dir, INITIAL_BOOK_STORE, r"*.txt"))
    print("Searching folder", bookshelf)
    books = glob.iglob(bookshelf)
    number_books = 0
    print('')
    start_time = time.time()
    for book in books:
        try:
            number_books += 1
            start_book = time.time()
            print("Filepath:",book)
            # get the book's id
            gutenberg_id = get_gutenberg_id(book)
            print("ID:",gutenberg_id)
            # check if book is valid novel by our definition
            if (not is_valid_novel_gutenberg(gutenberg_id, book)):
                print("Not a novel")
                print("Time for this book:", time.time() - start_book, "seconds")
                print('')
                continue
            # begin compiling metadata.  Metadata not finalized
            novel_metadata = {'gutenberg_id': gutenberg_id, 'corpus_name': 'gutenberg'}
            author = get_author_gutenberg(gutenberg_id)
            print("Author:",author)
            novel_metadata['author'] = author
            title = get_title_gutenberg(gutenberg_id)
            print("Title:",title)
            novel_metadata['title'] = title
            novel_metadata['date'] = get_publication_date(author, title, book, gutenberg_id)
            print("Date:",novel_metadata['date'])
            novel_metadata['country_publication'] = get_country_publication(author,
                title)
            print("Country:",novel_metadata['country_publication'])
            novel_metadata['author_gender'] = get_author_gender(author)
            print("Author Gender:",novel_metadata['author_gender'])
            novel_metadata['subject'] = get_subject_gutenberg(gutenberg_id)
            print("Subjects:",novel_metadata['subject'])
            # write to csv
            write_metadata(novel_metadata)
            print("wrote metadata")
            # copy text file to new folder
            copyfile(book, Path(current_dir, FINAL_BOOK_STORE, str(gutenberg_id) + r".txt"))
            print("Copied book")
            print("Time for this book:",time.time()-start_book, "seconds")
            print('')
        except Exception as exception:
            print("Ran into exception:", type(exception))
            print(exception)
            print("")
            continue
    end_time = time.time()
    print("Done!")
    print("No. Books:", number_books)
    print("Total Time:", end_time-start_time, "seconds")
    print("Average Time per Book", (end_time-start_time)/number_books)


def get_gutenberg_id(filepath):
    """
    For file with filepath get the gutenberg id of that book.  Should not be hard because gutenberg
    literally names files by id

    >>> from gender_novels import corpus_gen
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> get_gutenberg_id(Path(current_dir, r"corpora/test_books_30/44-0.txt"))
    44
    >>> get_gutenberg_id(Path(current_dir, r"corpora/test_books_30/11000-0.txt"))
    11000

    :param filepath: Path
    :return: int
    """
    filename = Path(filepath).name
    filename = filename.replace(r"-0.txt",'')
    return int(filename)


def is_valid_novel_gutenberg(gutenberg_id, filepath):
    """
    Determines whether book with this gutenberg id is actually a "novel".  Returns false if the book
    is not or doesn't actually exist.
    Should check:
    If book is English
    If book is under public domain
    If book is a "novel"
    if novel is in correct publication range
    That novel is not a translation

    >>> from gender_novels.corpus_gen import is_valid_novel_gutenberg
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> is_valid_novel_gutenberg(32, Path(current_dir, r"corpora/test_books_30/32-0.txt"))
    Herland
    True
    >>> is_valid_novel_gutenberg(11000, Path(current_dir, r"corpora/test_books_30/11000-0.txt"))
    An Old Babylonian Version of the Gilgamesh Epic
    Bad subject
    False
    >>> is_valid_novel_gutenberg(1404, Path(current_dir, r"corpora/test_books_30/1404-0.txt"))
    The Federalist Papers
    False

    :param gutenberg_id: int
    :return: boolean
    TODO: increase selectivity (Federalist Papers still failing doctest)
    """
    title = get_title_gutenberg(gutenberg_id)
    print(title)
    if language_invalidates_entry(gutenberg_id):
        print("Not in English")
        return False
    if rights_invalidate_entry(gutenberg_id):
        print("Not public domain")
        return False
    if subject_invalidates_entry(gutenberg_id):
        print("Bad subject")
        return False
    if date_invalidates_entry(gutenberg_id, filepath):
        print("Not in date range")
        return False
    # title = get_title_gutenberg(gutenberg_id)
    if title_invalidates_entry(title):
        print("Invalid title")
        return False
    text = get_novel_text_gutenberg_with_boilerplate(filepath)
    if text_invalidates_entry(text):
        print("Something wrong with text")
        return False
    return True


def language_invalidates_entry(gutenberg_id):
    """
    Returns False if book with gutenberg id is in English, True otherwise

    >>> from gender_novels.corpus_gen import language_invalidates_entry
    >>> language_invalidates_entry(46) # A Christmas Carol
    False
    >>> language_invalidates_entry(27217) # Some Chinese thing
    True

    :param gutenberg_id: int
    :return: boolean
    """
    language = list(get_metadata('language', gutenberg_id))[0]
    if (language != 'en'):
        return True
    else:
        return False


def rights_invalidate_entry(gutenberg_id):
    """
    Returns False if book with gutenberg id is in public domain in US, True otherwise

    >>> from gender_novels.corpus_gen import rights_invalidate_entry
    >>> rights_invalidate_entry(5200) # Metamorphosis by Franz Kafka
    True
    >>> rights_invalidate_entry(8066) # The Bible, King James version, Book 66: Revelation
    False

    :param gutenberg_id: int
    :return: boolean
    """
    rights = get_metadata('rights', gutenberg_id)
    if ('Public domain in the USA.' in rights):
        return False
    else:
        return True


def subject_invalidates_entry(gutenberg_id):
    """
    Checks if the Gutenberg subject indicates that the book is not a novel

    >>> from gender_novels.corpus_gen import subject_invalidates_entry
    >>> subject_invalidates_entry(2240) # Much Ado About Nothing
    True
    >>> subject_invalidates_entry(33) # The Scarlet Letter
    False

    :param gutenberg_id: int
    :return: boolean
    """

    subjects = get_subject_gutenberg(gutenberg_id)
    for subject in subjects:
        for word in SUBJECTS_TO_IGNORE:
            if ((subject.lower()).find(word) != -1):
                return True
    return False


def date_invalidates_entry(gutenberg_id, filepath):
    """
    Checks if book with gutenberg id is in correct date range.  If it can't get the date, simply returns False
    >>> from gender_novels.corpus_gen import date_invalidates_entry
    >>> date_invalidates_entry(33, r"corpora/sample_novels/texts/hawthorne_scarlet.txt")
    False

    :param gutenberg_id: int
    :param filepath: str
    :return: boolean
    """

    author = get_author_gutenberg(gutenberg_id)
    title = get_title_gutenberg(gutenberg_id)
    try:
        date = int(get_publication_date(author, title, filepath, gutenberg_id))
        if ((date < 1770 or date > 1922)):
            return True
        else:
            return False
    except TypeError:
        return False


def title_invalidates_entry(title):
    """
    Determines if the title contains phrases that indicate that the book is invalid

    >>> from gender_novels.corpus_gen import title_invalidates_entry
    >>> title_invalidates_entry("Index of the Project Gutenberg Works of Michael Cuthbert")
    True
    >>> title_invalidates_entry("Pride and Prejudice")
    False

    :param title: str
    :return: boolean
    """
    title = title.lower()
    if (title.find("index of the project gutenberg ") != -1):
        # print("Was an index")
        return True
    if (title.find("complete project gutenberg") != -1):
        # print("Was a compilation thing")
        return True
    if (title.find("translated by ") != -1):
        # print("Was a translation")
        return True
    return False


def text_invalidates_entry(text):
    """
    Determine if there is anything obvious in the text that would invalidate it as a valid novel

    >>> from gender_novels.corpus_gen import text_invalidates_entry
    >>> text_invalidates_entry("Translator: George Fyler Townsend")
    True
    >>> from gender_novels.corpus_gen import get_novel_text_gutenberg
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> filepath = Path(current_dir, r"corpora/sample_novels/texts/hawthorne_scarlet.txt")
    >>> scarlet_letter = get_novel_text_gutenberg(filepath)
    >>> text_invalidates_entry(scarlet_letter)
    False

    :param text: str
    :return: boolean
    """
    if (text.find("Translator: ", 0, 650) != -1):
        return True
    text = strip_headers(text)
    text_length = len(text)
    # Animal Farm is roughly 166700 characters including boilerplate
    # Guiness World Records states that the longest novel is 9,609,000 characters long
    if (text_length < 140000 or text_length > 9609000 ):
        return True
    return False


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

    return list(get_metadata('author', gutenberg_id))


def get_title_gutenberg(gutenberg_id):
    """
    Gets title for novel with this gutenberg id

    >>> from gender_novels import corpus_gen
    >>> get_title_gutenberg(33)
    'The Scarlet Letter'

    """

    title = list(get_metadata('title', gutenberg_id))[0]
    for sep in TRUNCATORS:
        title = title.split(sep,1)[0]
    return title


def get_novel_text_gutenberg(filepath):
    """
    Extract text as as string from file, with boilerplate removed

    >>> from gender_novels.corpus_gen import get_novel_text_gutenberg
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> book = get_novel_text_gutenberg(Path(current_dir, r"corpora/test_books_30/32-0.txt"))
    >>> book[:7]
    'HERLAND'

    :param filepath: str
    :return: str
    """
    return strip_headers(get_novel_text_gutenberg_with_boilerplate(filepath)).strip()

def get_novel_text_gutenberg_with_boilerplate(filepath):
    """
    Extract text as as string from file

    >>> from gender_novels.corpus_gen import get_novel_text_gutenberg
    >>> import os
    >>> current_dir = os.path.abspath(os.path.dirname(__file__))
    >>> book = get_novel_text_gutenberg(Path(current_dir, r"corpora/test_books_30/32-0.txt"))
    >>> book[:3]
    'The'

    TODO: wait, why is is it still removing boilerplate

    :param filepath: str
    :return: str
    """
    if common.get_text_file_encoding(filepath) not in {'utf-8', 'UTF-8-SIG'}:
        # target_path = Path(Path(filepath).parent, r"converted", Path(filepath).name)
        common.convert_text_file_to_new_encoding(source_path=filepath,
                                                 target_path=filepath,
                                                 target_encoding='utf-8')
    with open(filepath, mode='r', encoding='utf8') as text:
        text_with_headers = text.read()
    return text_with_headers


def get_publication_date(author, title, filepath, gutenberg_id = None):
    """
    For a given novel with id gutenberg_id this function attempts a variety of
    methods to try and find the publication date
    If it can't returns None

    >>> from gender_novels import corpus_gen
    >>> get_publication_date("Hawthorne, Nathaniel", "The Scarlet Letter",
    ... r"corpora/sample_novels/texts/hawthorne_scarlet.txt", 33)
    1850

    # >>> from gender_novels import corpus_gen
    # >>> get_publication_date("Dick, Phillip K.", "Mr. Spaceship", 32522)
    # 1953

    :param author: list
    :param title: str
    :param gutenberg_id: int
    :param filepath: str
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
    For a given novel with this author and title this function attempts to pull the publication
    year from Wikidata Otherwise returns None
    N.B.: This fails if the title is even slightly wrong (e.g. The Adventures of Huckleberry Finn vs
    Adventures of Huckleberry Finn).  Should it be tried to fix that?
    Function also doesn't use author parameter

    >>> from gender_novels import corpus_gen
    >>> get_publication_date_wikidata("Bacon, Francis", "Novum Organum")
    1620
    >>> get_publication_date_wikidata("Duan, Mingfei", "How I Became a Billionaire and also the President")

    >>> get_publication_date_wikidata("Austen, Jane", "Persuasion")
    1818
    >>> get_publication_date_wikidata("Scott, Walter", "Ivanhoe: A Romance")
    1820

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
        try:
            if (title == title.split(":", 1)[0].split(";,1")[0]):
                return None
            else:
                return get_publication_date_wikidata(author, title.split(":", 1)[0].split(";,1")[0])
        except (pywikibot.exceptions.NoPage):
            return None
    except(pywikibot.exceptions.InvalidTitle):
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
        match = re.search(r"\d{4}", novel_text[:3000])
        if (match != None):
            year = int(match.group(0))
            if (year < 2000 and year > 1492):
                return year
            else:
                return None
        else: return None
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
        try:
            if (title == title.split(":", 1)[0].split(";,1")[0]):
                return None
            else:
                return get_country_publication_wikidata(author, title.split(":", 1)[0].split(";,1")[0])
        except (pywikibot.exceptions.NoPage):
            return None
    except(pywikibot.exceptions.InvalidTitle):
        return None

    # try to match country_id to major English-speaking countries
    if country_id in COUNTRY_ID_TO_NAME:
        return COUNTRY_ID_TO_NAME[country_id]

    # if not try look up wikidata page of country with that id to try and get short name
    try:
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
    except (KeyError, pywikibot.exceptions.NoPage, pywikibot.exceptions.InvalidTitle):
        #if that doesn't work just get one of the aliases. Name may be awkwardly long but should be consistent
        country = dictionary['aliases']['en'][-1]
        return country


def format_author(author):
    """
    Formats a string in the form "Lastname, Firstname" into "Firstname Lastname"
    and a string in the form "Lastname, Firstname Middle" into "Firstname Middle Lastname"
    and a string in the form "Lastname, F. M. (First Middle)" into "First Middle Lastname"
    and a string in the form "Lastname, Firstname, Sfx." into "Firstname Lastname, Sfx."
    If string is not in any of the above forms just returns the string.

    >>> from gender_novels.corpus_gen import format_author
    >>> format_author("Washington, George")
    'George Washington'
    >>> format_author("Hurston, Zora Neale")
    'Zora Neale Hurston'
    >>> format_author('King, Martin Luther, Jr.')
    'Martin Luther King, Jr.'
    >>> format_author("Montgomery, L. M. (Lucy Maud)")
    'Lucy Maud Montgomery'
    >>> format_author("Socrates")
    'Socrates'

    :param author: str
    :return: str
    """

    author_formatted = ''
    try:
        match = re.match(AUTHOR_NAME_REGEX, author)
        first_name = match.groupdict()['first_name']
        if (match.groupdict()['real_name'] != None):
            first_name = match.groupdict()['real_name']
        author_formatted = first_name + " " + match.groupdict()['last_name']
        if (match.groupdict()['suffix'] != None):
            author_formatted += match.groupdict()['suffix']
    except (TypeError, AttributeError):
        author_formatted = author
    return author_formatted

def get_author_gender(authors):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary', or 'both' (if there are multiple
    authors of different genders)
    Returns 'unknown' if it fails
    #TODO: should get functions that fail to find anything return 'unknown'
    #TODO: 'both' is ambiguous; Does it mean both female and male?  female and unknown?
    #TODO: male and nonbinary?

    >>> from gender_novels.corpus_gen import get_author_gender
    >>> get_author_gender(["Hawthorne, Nathaniel"])
    'male'
    >>> get_author_gender(["Cuthbert, Michael"])
    'male'
    >>> get_author_gender(["Duan, Mingfei"])
    'unknown'
    >>> get_author_gender(["Collins, Suzanne", "Riordan, Rick"])
    'both'
    >>> get_author_gender(["Shelley, Mary", "Austen, Jane"])
    'female'

    # should return 'both' because it doesn't recognize my name

    >>> get_author_gender(['Shakespeare, William', "Duan, Mingfei"])
    'both'
    >>> get_author_gender(["Montgomery, L. M. (Lucy Maud)"])
    'female'
    >>> get_author_gender(['Shelley, Mary Wollstonecraft'])
    'female'

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
            author_gender = get_author_gender_guesser(author)
        if author_gender == None:
            return 'unknown'
    else:
        author_gender = get_author_gender([authors[0]])
        for author in authors:
            if (get_author_gender([author]) != author_gender):
                author_gender = 'both'
    return author_gender

def get_author_gender_wikidata(author):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary' from wikidata
    If it fails returns None
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
    author_formatted = format_author(author)
    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, author_formatted)
        item = pywikibot.ItemPage.fromPage(page)
        dictionary = item.get()
        clm_dict = dictionary["claims"]
        return get_gender_from_wiki_claims(clm_dict)
    except (pywikibot.exceptions.NoPage, pywikibot.exceptions.InvalidTitle):
        return None

def get_gender_from_wiki_claims(clm_dict):
    """
    From clim_dict produced by pywikibot from a page, tries to extract the gender of the object of the page
    If it fails returns None
    N.B. Wikidata's categories for transgender male and female are treated as male and female, respectively

    >>> from gender_novels.corpus_gen import get_gender_from_wiki_claims
    >>> site = pywikibot.Site("en", "wikipedia")
    >>> page = pywikibot.Page(site, 'Zeus')
    >>> item = pywikibot.ItemPage.fromPage(page)
    >>> dictionary = item.get()
    >>> clm_dict = dictionary["claims"]
    >>> get_gender_from_wiki_claims(clm_dict)
    'male'

    :param clm_dict: dict
    :return: str
    """
    try:
        clm_list = clm_dict["P21"]
        gender_id = None
        for clm in clm_list:
            clm_trgt = clm.getTarget()
            gender_id = clm_trgt.id
        if (gender_id == 'Q6581097' or gender_id == 'Q2449503'):
            return 'male'
        if (gender_id == 'Q6581072' or gender_id == 'Q1052281'):
            return 'female'
        if (gender_id == 'Q1097630'):
            return 'non-binary'
    except (KeyError):
        return None

def get_author_gender_guesser(author):
    """
    Tries to get gender of author, 'female', 'male', 'non-binary' from the gender guesser module

    >>> from gender_novels.corpus_gen import get_author_gender_guesser
    >>> get_author_gender_guesser("Cuthbert, Michael")
    'male'
    >>> get_author_gender_guesser("Li, Michelle")
    'female'
    >>> get_author_gender_guesser("Duan, Mingfei") # should return None


    :param author: str
    :return: str
    """

    first_name = format_author(author).split()[0]
    guesser = gender_guesser.Detector()
    gender_guess = guesser.get_gender(first_name)
    if (gender_guess == 'andy' or gender_guess == 'unknown'):
        return None
    if (gender_guess == 'male' or gender_guess == 'mostly_male'):
        return 'male'
    if (gender_guess == 'female' or gender_guess == 'mostly_female'):
        return 'female'


def get_subject_gutenberg(gutenberg_id):
    """
    Tries to get subjects

    >>> from gender_novels import corpus_gen
    >>> get_subject_gutenberg(5200)
    ['Metamorphosis -- Fiction', 'PT', 'Psychological fiction']

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
    current_dir = os.path.abspath(os.path.dirname(__file__))
    corpus = novel_metadata['corpus_name']
    path = Path(current_dir, 'corpora', corpus, f'{corpus}.csv')
    with open(path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=METADATA_LIST)
        writer.writerow(novel_metadata)

if __name__ == '__main__':
    # from dh_testers.testRunner import main_test
    # main_test()
    generate_corpus_gutenberg()
