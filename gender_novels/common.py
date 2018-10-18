import os
import urllib.request

from pathlib import Path

DEBUG = False

BASE_PATH = Path(os.path.abspath(os.path.dirname(__file__)))
GUTENBERG_METADATA_PATH = Path('corpora', 'gutenberg', 'gutenberg.csv')
METADATA_LIST = ['gutenberg_id', 'author', 'date', 'title', 'country_publication', 'author_gender',
                 'subject', 'corpus_name', 'notes']

# books from gutenberg downloaded from Dropbox folder shared by Keith
INITIAL_BOOK_STORE = r'corpora/test_books_30'
# plus some extras
FINAL_BOOK_STORE = r'test_corpus'
AUTHOR_NAME_REGEX = r"(?P<last_name>(\w+ )*\w*)\, (?P<first_name>(\w+\.* )*(\w\.*)*)(?P<suffix>\, \w+\.)*(\((?P<real_name>(\w+ )*\w*)\))*"
import codecs
outputDir = 'converted'

#TODO(elsa): Investigate doctest errors in this file, may be a result of my own system, not actual code errors

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
        >>> type(corpus_metadata)
        <class 'list'>

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
            if not local_path.endswith('gender_novels'):
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
        file = open(local_base_path.joinpath(file_path), mode='r', encoding='utf8')

        if current_file_type == '.csv':
            result = file.readlines()
        elif current_file_type == '.txt':
            try:
                result = file.read()
            except UnicodeDecodeError as err:
                print(f'File loading error with {file_path}.')
                raise err

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

def get_text_file_encoding(filepath):
    """
    For text file at filepath returns the text encoding as a string (e.g. 'utf-8')

    >>> get_text_file_encoding(r"corpora/sample_novels/texts/hawthorne_scarlet.txt")
    'UTF-8-SIG'

    Note: For files containing only ascii characters, this function will return 'ascii' even if
    the file was encoded with utf-8
    >>> text = 'here is an ascii text'
    >>> file_path = Path(BASE_PATH, 'example_file.txt')
    >>> with codecs.open(file_path, 'w', 'utf-8') as source: source.write(text)
    >>> get_text_file_encoding(file_path)
    'ascii'
    >>> import os
    >>> os.remove(file_path)

    :param filepath: fstr
    :return: str
    """

    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()

    with open(filepath, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done: break
        detector.close()
    return detector.result['encoding']


def convert_text_file_to_new_encoding(source_path, target_path, target_encoding):
    """
    Converts a text file in source_path to the specified encoding in target_encoding
    Note: Currentyl only supports encodings utf-8, ascii and iso-8859-1

    :param source_path: str or Path
    :param target_path: str or Path
    :param target_encoding: str

    >>> text = ' ¶¶¶¶ here is a test file'
    >>> source_path = Path(BASE_PATH, 'source_file.txt')
    >>> target_path = Path(BASE_PATH, 'target_file.txt')
    >>> with codecs.open(source_path, 'w', 'iso-8859-1') as source: source.write(text)
    >>> get_text_file_encoding(source_path)
    'ISO-8859-1'
    >>> convert_text_file_to_new_encoding(source_path, target_path, target_encoding='utf-8')
    >>> get_text_file_encoding(target_path)
    'utf-8'
    >>> import os
    >>> os.remove(source_path)
    >>> os.remove(target_path)

    :return:
    """

    valid_encodings = ['utf-8', 'utf8', 'UTF-8-SIG', 'ascii', 'iso-8859-1', 'ISO-8859-1']

    # if the source_path or target_path is a string, turn to Path object.
    if isinstance(source_path, str):
        source_path = Path(source_path)
    if isinstance(target_path, str):
        target_path = Path(target_path)

    # check if source and target encodings are valid
    source_encoding = get_text_file_encoding(source_path)
    if source_encoding not in valid_encodings:
        raise ValueError('convert_text_file_to_new_encoding() only supports the following source '
                         f'encodings: {valid_encodings} but not {source_encoding}.')
    if target_encoding not in valid_encodings:
        raise ValueError('convert_text_file_to_new_encoding() only supports the following target '
                         f'encodings: {valid_encodings} but not {target_encoding}.')

    # print warning if filenames don't end in .txt
    if not source_path.parts[-1].endswith('.txt') or not target_path.parts[-1].endswith('.txt'):
        print(f"WARNING: Changing encoding to {target_encoding} on a file that does not end with "
              f".txt. Source: {source_path}. Target: {target_path}")

    with codecs.open(source_path, 'rU', encoding=source_encoding) as source_file:
        text = source_file.read()
    with codecs.open(target_path, 'w', encoding=target_encoding) as target_file:
        target_file.write(text)

if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
