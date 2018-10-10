import os
import urllib.request

from pathlib import Path

DEBUG = False


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



if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
