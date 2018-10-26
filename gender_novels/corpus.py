import csv
from pathlib import Path
from collections import Counter

from gender_novels import common
from gender_novels.novel import Novel



class Corpus(common.FileLoaderMixin):
    """The corpus class is used to load the metadata and full
    texts of all novels in a corpus

    Once loaded, each corpus contains a list of Novel objects

    >>> from gender_novels.corpus import Corpus
    >>> c = Corpus('sample_novels')
    >>> type(c.novels), len(c)
    (<class 'list'>, 99)

    >>> c.novels[0].author
    'Aanrud, Hans'

    You can use 'test_corpus' to load a test corpus of 10 novels:
    >>> test_corpus = Corpus('test_corpus')
    >>> len(test_corpus)
    10

    """

    def __init__(self, corpus_name=None):
        self.corpus_name = corpus_name
        if self.corpus_name == 'gutenberg':
            self._download_gutenberg_if_not_locally_available()

        self.load_test_corpus = False
        if self.corpus_name == 'test_corpus':
            self.load_test_corpus = True
            self.corpus_name = 'sample_novels'
        self.novels = []
        if corpus_name is not None:
            self.relative_corpus_path = Path('corpora', self.corpus_name)
            self.novels = self._load_novels()

    def _download_gutenberg_if_not_locally_available(self):
        """
        Checks if the gutenberg corpus is available locally. If not, downloads the corpus
        and extracts it to corpora/gutenberg

        No tests because the function depends on user input

        :return:
        """

        import os
        gutenberg_path = Path(common.BASE_PATH, 'corpora', 'gutenberg')

        # if there are more than 4000 text files available, we know that the corpus was downloaded
        # and can return
        try:
            no_gutenberg_novels=  len(os.listdir(Path(gutenberg_path, 'texts')))
            if no_gutenberg_novels > 4000:
                gutenberg_available = True
            else:
                gutenberg_available = False
        # if the texts path was not found, we know that we need to download the corpus
        except FileNotFoundError:
            gutenberg_available = False

        if not gutenberg_available:

            print("The Project Gutenberg corpus is currently not available on your system.",
                  "It consists of more than 4000 novels and 1.8 GB of data.")
            download_prompt = input(
                  "If you want to download the corpus, please enter (y). Any other input will "
                  "terminate the program: ")
            if not download_prompt in ['y', '(y)']:
                raise ValueError("Project Gutenberg corpus will not be downloaded.")

            import zipfile
            import urllib
            url = 'https://s3-us-west-2.amazonaws.com/gutenberg-cache/gutenberg_corpus.zip'
            urllib.request.urlretrieve(url, 'gutenberg_corpus.zip')
            zipf = zipfile.ZipFile('gutenberg_corpus.zip')
            if not os.path.isdir(gutenberg_path):
                os.mkdir(gutenberg_path)
            zipf.extractall(gutenberg_path)
            os.remove('gutenberg_corpus.zip')

            # check that we now have 4000 novels available
            try:
                no_gutenberg_novels = len(os.listdir(Path(gutenberg_path, 'texts')))
                print(f'Successfully downloaded {no_gutenberg_novels} novels.')
            except FileNotFoundError:
                raise FileNotFoundError("Something went wrong while downloading the gutenberg"
                                        "corpus.")



    def __len__(self):
        """
        For convenience: returns the number of novels in
        the corpus.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> len(c)
        99

        >>> female_corpus = c.filter_by_gender('female')
        >>> len(female_corpus)
        39

        :return: int
        """
        return len(self.novels)

    def __iter__(self):
        """
        Yield each of the novels from the .novels list.

        For convenience.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> titles = []
        >>> for this_novel in c:
        ...    titles.append(this_novel.title)
        >>> titles #doctest: +ELLIPSIS
        ['Lisbeth Longfrock', 'Flatland', ... 'The Heir of Redclyffe']

        """
        for this_novel in self.novels:
            yield this_novel

    def __eq__(self, other):
        """
        Returns true if both corpora contain the same novels
        Note: ignores differences in the corpus name as that attribute is not used apart from
        initializing a corpus.
        Presumes the novels to be sorted. (They get sorted by the initializer)

        >>> from gender_novels.corpus import Corpus
        >>> sample_corpus = Corpus('sample_novels')
        >>> sample_corpus.novels = sample_corpus.novels[:20]
        >>> male_corpus = sample_corpus.filter_by_gender('male')
        >>> female_corpus = sample_corpus.filter_by_gender('female')
        >>> merged_corpus = male_corpus + female_corpus
        >>> merged_corpus == sample_corpus
        True
        >>> sample_corpus == merged_corpus + male_corpus
        False

        :return: bool
        """

        if not isinstance(other, Corpus):
            raise NotImplementedError("Only a Corpus can be added to another Corpus.")

        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self.novels[i] != other.novels[i]:
                return False

        return True

    def __add__(self, other):
        """
        Adds two corpora together and returns a copy of the result
        Note: retains the name of the first corpus

        >>> from gender_novels.corpus import Corpus
        >>> sample_corpus = Corpus('sample_novels')
        >>> sample_corpus.novels = sample_corpus.novels[:20]
        >>> male_corpus = sample_corpus.filter_by_gender('male')
        >>> female_corpus = sample_corpus.filter_by_gender('female')
        >>> merged_corpus = male_corpus + female_corpus
        >>> merged_corpus == sample_corpus
        True

        :return: Corpus
        """
        if not isinstance(other, Corpus):
            raise NotImplementedError("Only a Corpus can be added to another Corpus.")

        output_corpus = self.clone()
        for novel in other:
            output_corpus.novels.append(novel)
        output_corpus.novels = sorted(output_corpus.novels)

        return output_corpus

    def clone(self):
        """
        Return a copy of this Corpus

        >>> from gender_novels.corpus import Corpus
        >>> sample_corpus = Corpus('sample_novels')
        >>> corpus_copy = sample_corpus.clone()
        >>> len(corpus_copy) == len(sample_corpus)
        True

        :return: Corpus
        """
        corpus_copy = Corpus()
        corpus_copy.corpus_name = self.corpus_name
        corpus_copy.novels = self.novels[:]
        return corpus_copy

    def _load_novels(self):
        novels = []

        relative_csv_path = (self.relative_corpus_path
                             / f'{self.corpus_name}.csv')
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
            this_novel = Novel(novel_metadata_dict=novel_metadata)
            novels.append(this_novel)
            if self.load_test_corpus and len(novels) == 10:
                break

        return sorted(novels)

    def count_authors_by_gender(self, gender):
        """
        This function returns the number of authors with the
        specified gender (male, female, non-binary, unknown)

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.count_authors_by_gender('female')
        39

        Accepted inputs are 'male', 'female', 'non-binary' and 'unknown'
        but no abbreviations.

        >>> c.count_authors_by_gender('m')
        Traceback (most recent call last):
        ValueError: Gender must be male, female, non-binary, unknown but not m.

        :rtype: int
        """
        filtered_corpus = self.filter_by_gender(gender)
        return len(filtered_corpus)

    def filter_by_gender(self, gender):
        """
        Return a new Corpus object that contains only authors whose gender
        matches gender_filter.

        Accepted inputs are 'male', 'female', 'non-binary' and 'unknown'
        but no abbreviations.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> female_corpus = c.filter_by_gender('female')
        >>> len(female_corpus)
        39
        >>> female_corpus.novels[0].title
        'The Indiscreet Letter'

        >>> male_corpus = c.filter_by_gender('male')
        >>> len(male_corpus)
        59

        >>> male_corpus.novels[0].title
        'Lisbeth Longfrock'

        :param gender: gender name
        :return: Corpus
        """
        supported_genders = ('male', 'female', 'non-binary', 'unknown')
        if gender not in supported_genders:
            raise ValueError(
                f'Gender must be {", ".join(supported_genders)} '
                + f'but not {gender}.')

        corpus_copy = self.clone()
        corpus_copy.novels = []

        for this_novel in self.novels:
            # check if all novels have an author_gender attribute
            if not hasattr(this_novel, 'author_gender'):
                err = f'Cannot count author genders in {self.corpus_name} '
                err += 'corpus. The novel '
                err += f'{this_novel.title} by {this_novel.author} lacks '
                err += 'the attribute "author_gender."'
                raise AttributeError(err)
            if this_novel.author_gender == gender:
                corpus_copy.novels.append(this_novel)

        return corpus_copy

    def get_wordcount_counter(self):
        """
        This function returns a Counter telling how many times a word appears in an entire
        corpus

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_wordcount_counter()['fire']
        2269

        """
        corpus_counter = Counter()
        for current_novel in self.novels:
            novel_counter = current_novel.get_wordcount_counter()
            corpus_counter += novel_counter
        return corpus_counter

    def get_corpus_metadata(self):
        """
        This function returns a sorted list of all metadata fields
        in the corpus as strings. This is different from the get_metadata_fields;
        this returns the fields which are specific to the corpus it is being called on.
        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_corpus_metadata()
        ['author', 'author_gender', 'corpus_name', 'country_publication', 'date', 'filename', 'notes', 'title']

        :return: list
        """
        metadata_fields = set()
        for novel in self.novels:
            for field in getmembers(novel):
                metadata_fields.add(field)
        return sorted(list(metadata_fields))

    def get_field_vals(self,field):
        """
        This function returns a sorted list of all values for a
        particular metadata field as strings.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_field_vals('corpus_name')
        ['sample_novels']

        :param field: str
        :return: list
        """
        metadata_fields = self.get_corpus_metadata()

        if field not in metadata_fields:
            raise ValueError(
                f'\'{field}\' is not a valid metadata field for this corpus'
            )

        values = set()
        for novel in self.novels:
            values.add(getattr(novel,field))

        return sorted(list(values))

    def subcorpus(self,metadata_field,field_value):
        """
        This method takes a metadata field and value of that field and returns
        a new Corpus object which includes the subset of novels in the original
        Corpus that have the specified value for the specified field.

        Supported metadata fields are 'author', 'author_gender', 'corpus_name',
        'country_publication', 'date'

        >>> from gender_novels.corpus import Corpus

        >>> corp = Corpus('sample_novels')
        >>> female_corpus = corp.subcorpus('author_gender','female')
        >>> len(female_corpus)
        39
        >>> female_corpus.novels[0].title
        'The Indiscreet Letter'

        >>> male_corpus = corp.subcorpus('author_gender','male')
        >>> len(male_corpus)
        59
        >>> male_corpus.novels[0].title
        'Lisbeth Longfrock'

        >>> eighteen_fifty_corpus = corp.subcorpus('date','1850')
        >>> len(eighteen_fifty_corpus)
        1
        >>> eighteen_fifty_corpus.novels[0].title
        'The Scarlet Letter'

        >>> jane_austen_corpus = corp.subcorpus('author','Austen, Jane')
        >>> len(jane_austen_corpus)
        2
        >>> jane_austen_corpus.novels[0].title
        'Emma'

        >>> england_corpus = corp.subcorpus('country_publication','England')
        >>> len(england_corpus)
        51
        >>> england_corpus.novels[0].title
        'Flatland'

        :param metadata_field: str
        :param field_value: str
        :return: Corpus
        """

        supported_metadata_fields = ('author', 'author_gender', 'corpus_name',
                                     'country_publication', 'date')
        if metadata_field not in supported_metadata_fields:
            raise ValueError(
                f'Metadata field must be {", ".join(supported_metadata_fields)} '
                + f'but not {metadata_field}.')

        corpus_copy = self.clone()
        corpus_copy.novels = []

        #adds novels to corpus_copy
        if metadata_field == 'date':
            for this_novel in self.novels:
                if this_novel.date == int(field_value):
                    corpus_copy.novels.append(this_novel)
        else:
            for this_novel in self.novels:
                if getattr(this_novel,metadata_field) == field_value:
                    corpus_copy.novels.append(this_novel)

        if not corpus_copy:
            #displays for possible errors in field.value
            err = f'This corpus is empty. You may have mistyped something.'
            raise AttributeError(err)

        return corpus_copy

    def multi_filter(self,characteristic_dict):
        """
        This method takes a dictionary of metadata fields and corresponding values
        and returns a Corpus object which is the subcorpus of the input corpus which
        satisfies all the specified constraints.

        #>>> from gender_novels.corpus import Corpus
        #>>> c = Corpus('sample_novels')
        #>>> characteristics = {'author':'female',
                                'country_publication':'England'}
        #>>> subcorpus_multi_filtered = c.multi_filter(characteristics)
        #>>> female_subcorpus = c.filter_by_gender('female')
        #>>> subcorpus_repeated_method = female_subcorpus.Subcorpus('country_publication','England')
        #>>> subcorpus_multi_filtered == subcorpus_repeated_method
        True

        :param characteristic_dict: dict
        :return: Corpus
        """

        new_corp = self.clone()
        metadata_fields = self.get_corpus_metadata()

        for field in characteristic_dict:
            if field not in metadata_fields:
                raise ValueError(f'\'{field}\' is not a valid metadata field for this corpus')
            new_corp = new_corp.subcorpus(field, characteristic_dict[field])

        return new_corp

        #TODO: add date range support
        #TODO: apply all filters at once instead of recursing Subcorpus method


    def get_novel(self, metadata_field, field_val):
        """
        Returns a specific Novel object from self.novels that has metadata matching field_val for
        metadata_field.  Otherwise raises a ValueError.
        N.B. This function will only return the first novel in the self.novels (which is sorted as
        defined by the Novel.__lt__ function).  It should only be used if you're certain there is
        only one match in the Corpus or if you're not picky about which Novel you get.  If you want
        more selectivity use get_novel_multiple_fields, or if you want multiple novels use the subcorpus
        function.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_novel("author", "Dickens, Charles")
        <Novel (dickens_twocities)>
        >>> c.get_novel("date", '1857')
        <Novel (bronte_professor)>
        >>> try:
        ...     c.get_novel("meme_quality", "over 9000")
        ... except AttributeError as exception:
        ...     print(exception)
        Metadata field meme_quality invalid for this corpus

        :param metadata_field: str
        :param field_val: str/int
        :return: Novel
        """

        if metadata_field not in get_metadata_fields(self.corpus_name):
            raise AttributeError(f"Metadata field {metadata_field} invalid for this corpus")

        if (metadata_field == "date" or metadata_field == "gutenberg_id"):
            field_val = int(field_val)

        for novel in self.novels:
            if getattr(novel, metadata_field) == field_val:
                return novel

        raise ValueError("Novel not found")

    def get_novel_multiple_fields(self, metadata_dict):
        """
        Returns a specific Novel object from self.novels that has metadata that matches a partial
        dict of metadata.  Otherwise raises a ValueError.
        N.B. This method will only return the first novel in the self.novels (which is sorted as
        defined by the Novel.__lt__ function).  It should only be used if you're certain there is
        only one match in the Corpus or if you're not picky about which Novel you get.  If you want
        multiple novels use the subcorpus function.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_novel_multiple_fields({"author": "Dickens, Charles", "author_gender": "male"})
        <Novel (dickens_twocities)>
        >>> c.get_novel_multiple_fields({"author": "Chopin, Kate", "title": "The Awakening"})
        <Novel (chopin_awakening)>

        :param metadata_dict: dict
        :return: Novel
        """

        for field in metadata_dict.keys():
            if field not in get_metadata_fields(self.corpus_name):
                raise AttributeError(f"Metadata field {field} invalid for this corpus")

        for novel in self.novels:
            match = True
            for field, val in metadata_dict.items():
                if getattr(novel, field) != val:
                    match = False
            if match:
                return novel

        raise ValueError("Novel not found")


def get_metadata_fields(corpus_name):
    """
    Gives a list of all metadata fields for corpus
    >>> from gender_novels import corpus
    >>> corpus.get_metadata_fields('gutenberg')
    ['gutenberg_id', 'author', 'date', 'title', 'country_publication', 'author_gender', 'subject', 'corpus_name', 'notes']

    :param: corpus_name: str
    :return: list
    """
    if corpus_name == 'sample_novels':
        return ['author', 'date', 'title', 'country_publication', 'author_gender', 'filename', 'notes']
    else:
        return common.METADATA_LIST





if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
