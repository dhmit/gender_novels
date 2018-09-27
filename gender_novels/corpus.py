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
    (<class 'list'>, 19)
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
            novels.append(novel.Novel(novel_metadata_dict=novel_metadata))

        return novels

    def count_authors_by_gender(self, gender):
        """
        This function returns the number of authors with the
        specified gender (male, female, non-binary, unknown)

        >>> from gender_novels.corpus import Corpus
        >>> c = Corpus('sample_novels')
        >>> c.count_authors_by_gender('female')
        10

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

        >>> from gender_novels import corpus
        >>> c = corpus.Corpus('sample_novels')
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


if __name__ == '__main__':
    from dh_testers.testRunner import main_test
    main_test()
