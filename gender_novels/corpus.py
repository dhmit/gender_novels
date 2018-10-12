import csv
from pathlib import Path

from gender_novels import common
from gender_novels import novel

class Corpus(common.FileLoaderMixin):
    """The corpus class is used to load the metadata and full
    texts of all novels in a corpus

    Once loaded, each corpus contains a list of Novel objects

    >>> from gender_novels.corpus import Corpus
    >>> c = Corpus('sample_novels')
    >>> type(c.novels), len(c.novels)
    (<class 'list'>, 99)

    >>> c.novels[0].author
    'Alcott, Louisa May'
    """
    def __init__(self, corpus_name=None):
        self.corpus_name = corpus_name
        self.novels = []
        if corpus_name is not None:
            self.novels = self._load_novels()

    def __iter__(self):
        """
        Yield each of the novels from the .novels list.

        For convenience.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> for this_novel in c:
        ...     print(this_novel.title)
        Little Women
        Jo's Boys,...
        ...
        """
        for this_novel in self.novels:
            yield this_novel

    def clone(self):
        """
        Return a copy of this Corpus

        >>> from gender_novels.corpus import Corpus
        >>> sample_corpus = Corpus('sample_novels')
        >>> corpus_copy = sample_corpus.clone()
        >>> len(corpus_copy.novels) == len(sample_corpus.novels)
        True

        :return: Corpus
        """
        corpus_copy = Corpus()
        corpus_copy.corpus_name = self.corpus_name
        corpus_copy.novels = self.novels[:]
        return corpus_copy

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
            this_novel = novel.Novel(novel_metadata_dict=novel_metadata)
            novels.append(this_novel)

        return novels

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
        return len(filtered_corpus.novels)

    def filter_by_gender(self, gender):
        """
        Return a new Corpus object that contains only authors whose gender
        matches gender_filter.

        Accepted inputs are 'male', 'female', 'non-binary' and 'unknown'
        but no abbreviations.

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> female_corpus = c.filter_by_gender('female')
        >>> len(female_corpus.novels)
        38
        >>> female_corpus.novels[0].title
        'Little Women'

        >>> male_corpus = c.filter_by_gender('male')
        >>> len(male_corpus.novels)
        60

        >>> male_corpus.novels[0].title
        'Heart of Darkness'

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

        for novel in self.novels:
            # check if all novels have an author_gender attribute
            if not hasattr(novel, 'author_gender'):
                err = f'Cannot count author genders in {self.corpus_name} '
                err += 'corpus. The novel '
                err += f'{novel.title} by {novel.author} lacks '
                err += 'the attribute "author_gender."'
                raise AttributeError(err)
            if novel.author_gender == gender:
                corpus_copy.novels.append(novel)

        return corpus_copy



if __name__ == '__main__':

    corpus = Corpus('sample_novels')

    from dh_testers.testRunner import main_test
    main_test()
