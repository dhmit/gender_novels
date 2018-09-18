"""

This is a scratch file for short tests and experiments that you don't want
to share with other lab members

"""

from gender_novels.common import Corpus

corpus = Corpus('sample_novels')

for novel in corpus.novels:
    print(novel.author, novel.title)

austen_novel = corpus.novels[0]

austen_novel
