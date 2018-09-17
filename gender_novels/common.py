import csv
import os
import urllib.request
from pathlib import Path

DEBUG = False


class FileLoaderMixin:
    """ The FileLoaderMixin loads files either locally or
    remotely from Github (if run from an ipython notebook)

    Currently supported filetypes are: .csv, .txt
    """

    def load_file(self, file_path):
        """
        Loads csv and txt files either locally or remotely from Github.
        file_path can be string or Path object.

        When loading a txt file, load_file returns the text as a string

        >>> from pathlib import Path
        >>> from gender_novels import common

        >>> f = common.FileLoaderMixin()
        >>> novel_path = Path('corpora', 'sample_novels',
        ...                   'texts', 'austen_persuasion.txt')
        >>> novel_text = f.load_file(novel_path)
        >>> type(novel_text), len(novel_text)
        (<class 'str'>, 486253)

        csv files are returned as a list of strings, which can be
        further processed with Python's csv module

        >>> corpus_metadata_path = Path('corpora', 'sample_novels',
        ...                             'sample_novels.csv')
        >>> corpus_metadata = f.load_file(corpus_metadata_path)
        >>> type(corpus_metadata), len(corpus_metadata)
        (<class 'list'>, 5)

        If the file is not available locally (e.g. in an ipython notebook,
        it gets loaded from Github.

        >>> novel_text_local = f.load_file_locally(novel_path, '.txt')
        >>> novel_text_online = f.load_file_remotely(novel_path, '.txt')
        >>> novel_text_local == novel_text_online
        True

        file_path can be a string or Path object

        >>> import os
        >>> novel_path_str = os.sep.join(['corpora', 'sample_novels',
        ...                               'texts', 'austen_persuasion.txt'])
        >>> novel_text_str = f.load_file(novel_path_str)
        >>> novel_text == novel_text_str
        True

        Returns a str (txt file) or list of strs (csv file)
        """
        # if the file_path is a string, turn to Path object.
        if isinstance(file_path, str):
            file_path = Path(file_path)

        # make sure that we only try to load supported file types
        supported_file_types = {'.csv', '.txt'}
        current_file_type = file_path.parts[-1][file_path.parts[-1].rfind('.'):]
        if current_file_type not in supported_file_types:
            err = "The FileLoaderMixin currently supports "
            err += "{supported_file_types} but not {current_file_type}."
            raise ValueError(err)

        # check if we are working locally and in the correct directory
        # __file__ is only available if executed from a file but
        # not from an ipython shell or notebook
        # in those cases, the file has to be loaded remotely from github.
        try:
            local_path = os.path.abspath(os.path.dirname(__file__))
            is_local = True
            if not local_path.endswith('/gender_novels'):
                is_local = False
                warning = "WARNING: The FileLoaderMixin should be placed "
                warning += "in the main path of the gender_novels project."
                warning += f"It's currently in {local_path}. Until the Mixin "
                warning += "is in the correct path, files are loaded "
                warning += "from Github."
                print(warning)
        except NameError:
            is_local = False

        if is_local:
            if DEBUG:
                print(f'loading {file_path} locally.')
            return self.load_file_locally(file_path, current_file_type)
        else:
            if DEBUG:
                print(f'loading {file_path} remotely')
            return self.load_file_remotely(file_path, current_file_type)

    @staticmethod
    def load_file_locally(file_path, current_file_type):
        # I need a way of getting the local path to the base of the repo.
        # This file is currently in the base of the
        # repo so it returns the correct path. But it will change once
        # this function gets moved.
        local_base_path = Path(os.path.abspath(os.path.dirname(__file__)))
        file = open(local_base_path.joinpath(file_path), mode='r')

        if current_file_type == '.csv':
            result = file.readlines()
        elif current_file_type == '.txt':
            result = file.read()
        else:
            raise Exception(
                'Cannot load if current_file_type is not .csv or .txt')

        file.close()
        return result

    @staticmethod
    def load_file_remotely(file_path, current_file_type):
        base_path = ('https://raw.githubusercontent.com/dhmit/'
                     + 'gender_novels/master/gender_novels/')
        url = f'{base_path}/{file_path}'
        response = urllib.request.urlopen(url)
        encoding = response.headers.get_param('charset')

        if current_file_type == '.csv':
            return [line.decode(encoding) for line in response.readlines()]
        elif current_file_type == '.txt':
            text = response.read().decode(encoding)
            # When loading the text online, each end of line
            # has \r and \n -> replace with only \n
            return text.replace('\r\n', '\n')


class Corpus(FileLoaderMixin):
    """The corpus class is used to load the metadata and full
    texts of all novels in a corpus

    Once loaded, each corpus contains a list of Novel objects

    >>> from gender_novels.common import Corpus
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

        relative_csv_path = Path('corpora',
                                 self.corpus_name,
                                 f'{self.corpus_name}.csv')
        try:
            csv_file = self.load_file(relative_csv_path)
        except FileNotFoundError:
            err = "Could not find the metadata csv file for the "
            err += "'{self.corpus_name}' corpus in the expected location "
            err += f"({relative_csv_path})."
            raise FileNotFoundError(err)
        csv_reader = csv.DictReader(csv_file)

        for novel_metadata in csv_reader:
            novel_metadata['corpus_name'] = self.corpus_name
            novels.append(Novel(novel_metadata_dict=novel_metadata))

        return novels

    def count_authors_by_gender(self, gender):
        """
        This function returns the number of authors with the
        specified gender (male, female, non-binary, unknown)

        >>> from gender_novels.common import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.count_authors_by_gender('female')
        2

        Accepted inputs are 'male', 'female', 'non-binary' and 'unknown'
        but no abbreviations.

        >>> c.count_authors_by_gender('m')
        Traceback (most recent call last):
        ValueError: Gender must be male, female, non-binary, unknown but not m.

        :rtype: int
        """
        supported_genders = ('male', 'female', 'non-binary', 'unknown')
        if gender not in supported_genders:
            raise ValueError(
                f'Gender must be {", ".join(supported_genders)} '
                + f'but not {gender}.')

        # check if all novels have an author_gender attribute
        for novel in self.novels:
            if not hasattr(novel, 'author_gender'):
                err = f'Cannot count author genders in {self.corpus_name} '
                err += 'corpus. The novel '
                err += f'{novel.title} by {novel.author} lacks '
                err += 'the attribute "author_gender."'
                raise AttributeError(err)

        gender_count = sum([1 if novel.author_gender == gender
                            else 0 for novel in self.novels])

        return gender_count

    def load_sample_novels_by_authors(self):
        """ This function returns the texts of the four novels
        in the sample_novels corpus as a tuple

        This function is used for the first DH Lab demonstration.

        >>> from gender_novels import common
        >>> c = common.Corpus('sample_novels')
        >>> sample_texts = c.load_sample_novels_by_authors()
        >>> austen, dickens, eliot, hawthorne = sample_texts
        >>> len(austen)
        467018

        :rtype: tuple
        """

        if self.corpus_name != 'sample_novels':
            err = ("load_sample_novels_by_author can only be used with the 'sample_novels'",
                   f"corpus but not with '{self.corpus_name}'")
            raise ValueError(err)

        austen = self.novels[0].text
        dickens = self.novels[1].text
        eliot = self.novels[2].text
        hawthorne = self.novels[3].text

        return austen, dickens, eliot, hawthorne


class Novel(FileLoaderMixin):
    """ The Novel class loads and holds the full text and
    metadata (author, title, publication date) of a novel

    >>> from gender_novels import common
    >>> novel_metadata = {'author': 'Austen, Jane', 'title': 'Persuasion',
    ...                   'corpus_name': 'sample_novels', 'date': '1818',
    ...                   'filename': 'austen_persuasion.txt'}
    >>> novel = common.Novel(novel_metadata)
    >>> type(novel.text), len(novel.text)
    (<class 'str'>, 467018)
    """

    def __init__(self, novel_metadata_dict):

        if not hasattr(novel_metadata_dict, 'items'):
            raise ValueError(
                'novel_metadata_dict must be a dictionary or support .items()')

        # Check that the essential attributes for the novel exists.
        for key in ('author', 'date', 'title', 'corpus_name', 'filename'):
            if key not in novel_metadata_dict:
                raise ValueError(
                    f'novel_metadata_dict must have an entry for "{key}"')

        self.author = novel_metadata_dict['author']
        self.data = novel_metadata_dict['date']
        self.title = novel_metadata_dict['title']
        self.corpus_name = novel_metadata_dict['corpus_name']
        self.filename = novel_metadata_dict['filename']

        # optional attributes
        self.country_publication = novel_metadata_dict.get(
            'country_publication', None)
        self.author_gender = novel_metadata_dict.get('author_gender', None)
        self.notes = novel_metadata_dict.get('notes', None)

        if 'text' in novel_metadata_dict:
            self.text = novel_metadata_dict['text']
        else:
            self.text = self._load_novel_text()

    def _load_novel_text(self):
        """Loads the text of a novel and removes
        boilerplate at the beginning and end

        Currently only supports boilerplate removal for
        Project Gutenberg ebooks.

        :rtype: str
        """
        file_path = Path('corpora', self.corpus_name, 'texts', self.filename)

        try:
            text = self.load_file(file_path)
        except FileNotFoundError:
            err = "Could not find the novel text file "
            err += "at the expected location ({file_path})."
            raise FileNotFoundError(err)

        # Extract Project Gutenberg Boilerplate
        if text.find('*** START OF THIS PROJECT GUTENBERG EBOOK') > -1:
            end_intro_boilerplate = text.find(
                '*** START OF THIS PROJECT GUTENBERG EBOOK')
            # second set of *** indicates start
            start_novel = text.find('***', end_intro_boilerplate + 5) + 3
            end_novel = text.find('*** END OF THIS PROJECT GUTENBERG EBOOK')
            text = text[start_novel:end_novel]

        return text


if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
