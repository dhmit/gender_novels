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
    (<class 'list'>, 94)

    >>> c.novels[0].author
    'Aanrud, Hans'
    """

    def __init__(self, corpus_name=None):
        self.corpus_name = corpus_name
        self.novels = []
        if corpus_name is not None:
            self.relative_corpus_path = Path('corpora', self.corpus_name)
            self.novels = self._load_novels()

    def __len__(self):
        """
        For convenience: returns the number of novels in
        the corpus.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> len(c)
        94

        >>> female_corpus = c.filter_by_gender('female')
        >>> len(female_corpus)
        38

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
        load_test_corpus = False
        if self.corpus_name == 'test_corpus':
            load_test_corpus = True
            self.corpus_name = 'sample_novels'

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
            if load_test_corpus and len(novels) == 10:
                break

        return sorted(novels)

    def count_authors_by_gender(self, gender):
        """
        This function returns the number of authors with the
        specified gender (male, female, non-binary, unknown)

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.count_authors_by_gender('female')
        38

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
        38
        >>> female_corpus.novels[0].title
        'The Indiscreet Letter'

        >>> male_corpus = c.filter_by_gender('male')
        >>> len(male_corpus)
        55

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
        2069

        """
        c = Corpus('sample_novels')
        corpus_counter = Counter()
        for current_novel in c.novels:
            novel_counter = current_novel.get_wordcount_counter()
            corpus_counter += novel_counter
        return corpus_counter


    def get_novel(self, metadata_field, field_val):
        """
        Returns a specific Novel object from self.novels that has metadata matching field_val for
        metadata_field.
        N.B. This function will only return the first novel in the self.novels (which is sorted as
        defined by the Novel.__lt__ function).  It should only be used if you're certain there is
        only one match in the Corpus or if you're not picky about which Novel you get.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.get_novel("author", "Dickens, Charles")
        <Novel (dickens_twocities)>

        :param metadata_field: str
        :param field_val: str/int
        :return: Novel
        """

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
