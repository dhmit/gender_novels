import csv
import os
import urllib.request
from pathlib import Path

DEBUG = False


class FileLoaderMixin():
    """ The FileLoaderMixin loads files either locally or remotely from Github (if run from an ipython notebook)

    Currently supported filetypes are: .csv, .txt

    """

    def load_file(self, file_path):
        """
        Loads csv and txt files either locally or remotely from Github.
        file_path can be string or Path object.

        When loading a txt file, load_file returns the text as a string
        >>> f = FileLoaderMixin()
        >>> novel_path = Path('corpora', 'sample_novels', 'texts', 'austen_persuasion.txt')
        >>> novel_text = f.load_file(novel_path)
        >>> type(novel_text), len(novel_text)
        (<class 'str'>, 486253)

        csv files are returned as a list of strings, which can be further processed with Python's csv module
        >>> corpus_metadata_path = Path('corpora', 'sample_novels', 'sample_novels.csv')
        >>> corpus_metadata = f.load_file(corpus_metadata_path)
        >>> type(corpus_metadata), len(corpus_metadata)
        (<class 'list'>, 5)

        If the file is not available locally (e.g. in an ipython notebook, it gets loaded from Github.
        >>> novel_text_local = f._load_file_locally(novel_path, '.txt')
        >>> novel_text_online = f._load_file_remotely(novel_path, '.txt')
        >>> novel_text_local == novel_text_online
        True

        file_path can be a string or Path object
        >>> novel_path_str = os.path.join('corpora', 'sample_novels', 'texts', 'austen_persuasion.txt')
        >>> novel_text_str = f.load_file(novel_path_str)
        >>> novel_text == novel_text_str
        True

        :rtype: str (txt file) or list of str (csv file)

        """

        # if the file_path is a string, turn to Path object.
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # make sure that we only try to load supported file types
        supported_file_types = {'.csv', '.txt'}
        current_file_type = file_path.parts[-1][file_path.parts[-1].rfind('.'):]
        if current_file_type not in supported_file_types:
            err = f"The FileLoaderMixin currently supports {supported_file_types} but not {current_file_type}."
            raise ValueError(err)

        # check if we are working locally and in the correct directory
        # __file__ is only available if executed from a file but not from an ipython shell or notebook
        # in those cases, the file has to be loaded remotely from github.
        try:
            local_path = os.path.abspath(os.path.dirname(__file__))
            is_local = True
            if not local_path.endswith('/gender_novels'):
                is_local = False
                warning = "WARNING: The FileLoaderMixin should be placed in the main path of the gender_novels project."
                warning += f"It's currently in {local_path}. Until the Mixin is in the correct path, files are loaded "
                warning += "from Github."
                print(warning)
        except NameError:
            is_local = False

        if is_local:
            if DEBUG:
                print(f'loading {file_path} locally.')
            return self._load_file_locally(file_path, current_file_type)
        else:
            if DEBUG:
                print(f'loading {file_path} remotely')
            return self._load_file_remotely(file_path, current_file_type)

    def _load_file_locally(self, file_path, current_file_type):

        # I need a way of getting the local path to the base of the repo. This file is currently in the base of the
        # repo so it returns the correct path. But it will change once this function gets moved.
        local_base_path = Path(os.path.abspath(os.path.dirname(__file__)))
        file = open(local_base_path.joinpath(file_path), mode='r')

        if current_file_type == '.csv':
            result = file.readlines()
        elif current_file_type == '.txt':
            result = file.read()

        file.close()
        return result

    def _load_file_remotely(self, file_path, current_file_type):

        base_path = 'https://raw.githubusercontent.com/dhmit/gender_novels/master/'
        url = f'{base_path}/{file_path}'
        response = urllib.request.urlopen(url)
        encoding = response.headers.get_param('charset')

        if current_file_type == '.csv':
            return [line.decode(encoding) for line in response.readlines()]
        elif current_file_type == '.txt':
            text = response.read().decode(encoding)
            # When loading the text online, each end of line has \r and \n -> replace with only \n
            return text.replace('\r\n', '\n')


class Corpus(FileLoaderMixin):
    """ The corpus class is used to load the metadata and full texts of all novels in a corpus

    Once loaded, each corpus contains a list of Novel objects
    >>> c = Corpus('sample_novels')
    >>> type(c.novels), len(c.novels)
    (<class 'list'>, 4)
    >>> c.novels[0].author
    'Austen, Jane'

    """

    def __init__(self, corpus_name):
        self.corpus_name = corpus_name
        self.novels = self._load_novels()

    def _load_novels(self):

        novels = []

        relative_csv_path = Path('corpora', self.corpus_name, f'{self.corpus_name}.csv')
        try:
            csv_file = self.load_file(relative_csv_path)
        except FileNotFoundError:
            err = f"Could not find the metadata csv file for the '{self.corpus_name}' corpus in the expected location "
            err += f"({relative_csv_path})."
            raise FileNotFoundError(err)
        csv_reader = csv.DictReader(csv_file)

        for novel_metadata in csv_reader:
            novel_metadata['corpus_name'] = self.corpus_name
            novels.append(Novel(novel_metadata_dict=novel_metadata))

        return novels

    def count_authors_by_gender(self, gender):
        """
        This function returns the number of authors with the specified gender (male, female,
        unknown)

        >>> c = Corpus('sample_novels')
        >>> c.count_authors_by_gender('female')
        2

        # Accepted inputs are 'male', 'female', and 'unknown' but no abbreviations.
        >>> c.count_authors_by_gender('m')
        Traceback (most recent call last):
        ValueError: Gender must be "male", "female", or "unknown" but not m.

        :rtype: int
        """

        if gender not in {'male', 'female', 'unknown'}:
            raise ValueError(f'Gender must be "male", "female", or "unknown" but not {gender}.')

        # check if all novels have an author_gender attribute
        for novel in self.novels:
            if not hasattr(novel, 'author_gender'):
                err = f'Cannot count author genders in {self.corpus_name} corpus. The novel'
                err +=f'{novel.title} by {novel.author} lacks the attribute "author_gender."'
                raise AttributeError(err)

        gender_count = sum([1 if novel.author_gender==gender else 0 for novel in self.novels])

        return gender_count

    def load_sample_novels_by_authors(self):
        """ This function returns the texts of the four novels in the sample_novels corpus as a tuple
        This function is used for the first DH Lab demonstration.

        >>> from gender_novels import common
        >>> c = common.Corpus('sample_novels')
        >>> austen, dickens, eliot, hawthorne = c.load_sample_novels_by_authors()
        >>> len(austen)
        467018

        :rtype: tuple
        """

        assert self.corpus_name == 'sample_novels'

        austen = self.novels[0].text
        dickens = self.novels[1].text
        eliot = self.novels[2].text
        hawthorne = self.novels[3].text

        return austen, dickens, eliot, hawthorne


class Novel(FileLoaderMixin):
    """ The Novel class loads and holds the full text and metadata (author, title, publication date) of a novel

    >>> novel_metadata = {'author':'Austen, Jane', 'title':'Persuasion', 'corpus_name':'sample_novels', 'date': '1818'}
    >>> novel_metadata['filename'] = 'austen_persuasion.txt'
    >>> novel = Novel(novel_metadata)
    >>> type(novel.text), len(novel.text)
    (<class 'str'>, 467018)

    """

    def __init__(self, novel_metadata_dict):

        if not hasattr(novel_metadata_dict, 'items'):
            raise ValueError('novel_metadata_dict must be a dictionary or support .items()')

        # Check that the essential attributes for the novel exists.
        # Currently available attributes that are not checked are: country_publication, author_gender, and notes.
        for key in ('author', 'date', 'title', 'corpus_name', 'filename'):
            if key not in novel_metadata_dict:
                raise ValueError(f'novel_metadata_dict must have an entry for "{key}"')

        for k, v in novel_metadata_dict.items():
            setattr(self, k, v)

        if not hasattr(self, 'text'):
            self.text = self._load_novel_text()

    def _load_novel_text(self):
        """Loads the text of a novel and removes boilerplate at the beginning and end

        Currently only supports boilerplate removal for Project Gutenberg ebooks.

        :rtype: str
        """
        file_path = Path('corpora', self.corpus_name, 'texts', self.filename)

        try:
            text = self.load_file(file_path)
        except FileNotFoundError:
            err = f"Could not find the novel text file at the expected location ({file_path})."
            raise FileNotFoundError(err)

        # Extract Project Gutenberg Boilerplate
        if text.find('*** START OF THIS PROJECT GUTENBERG EBOOK') > -1:
            end_intro_boilerplate = text.find('*** START OF THIS PROJECT GUTENBERG EBOOK')
            start_novel = text.find('***', end_intro_boilerplate + 5) + 3 # second set of *** indicates start
            end_novel = text.find('*** END OF THIS PROJECT GUTENBERG EBOOK')
            text = text[start_novel:end_novel]

        return text



if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()

