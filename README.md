# Gender / Novels

## Analysis of Gender and Gender Relations in English-Language Novels, 1770-1922

This research project concerns the depiction of gender in historical English language novels, exploring how authors of various backgrounds and experiences described gender in their works.

Currently, we have analyzed a corpus of over 4,200 books from [Project Gutenberg](https://www.gutenberg.org/), an online book repository, utilizing programming methods we developed. Among our findings, we discovered the ratio of male pronouns to female pronouns, the most common words after male and female pronouns, and the distance between repetitions of male and female pronouns.

As of Summer 2019, the work on this project has been forked into two repos:
- The website presenting our research: https://github.com/dhmit/gender_novels_site
- The Gender Analysis Toolkit, https://github.com/dhmit/gender_analysis

If you would like to contribute to this project, please check out one of those follow-on projects!

*This MIT Digital Humanities Lab project is part of the [MIT/SHASS Programs in Digital Humanities](https://digitalhumanities.mit.edu/) funded by the [Mellon Foundation](https://www.mellon.org/).*

## Usage
To use our tools or contribute to the project, please view our guide to contributing, `CONTRIBUTING.md`. It includes information on how to install the tools we used as well as style guidelines for adding code. We are open to contributions and would love to see other people’s ideas, thoughts, and additions to this project, so feel free to leave comments or make a pull request!

## Navigating Gender / Novels

For anybody who wants to use our code, here’s a little outline of where everything is.
In the [`gender_novels/gender_novels`](https://github.com/dhmit/gender_novels/tree/master/gender_novels) folder, there are six folders: 

1. [`analysis`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/analysis) — programming files focused on textual analysis and research write-ups, including data visualizations and conclusions
2. [`corpora`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/corpora) — metadata information on each book (including author, title, publication year, etc.), including sample data sets and instructions for generating a [Gutenberg mirror](https://github.com/dhmit/gender_novels/tree/master/gender_novels/corpora/gutenberg_mirror_sample)
3. [`deployment`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/deployment) — this directory contains code for the original Gender/Novels website. This has now been forked and replaced with https://github.com/dhmit/gender_novels_site; we only maintain this code here for historical reasons.
4. [`pickle_data`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/pickle_data) — pickled data for various analyses to avoid running time-consuming computation
5. [`testing`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/testing) — files for code tests
6. [`tutorials`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/tutorials) — tutorials used by the lab to learn about various technical subjects needed to complete this project

For a user who’ll need some readily available methods for analyzing documents, the files you’ll most likely want are [`corpus.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/corpus.py) and [`novel.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/novel.py). These include methods used for loading and analyzing texts from the corpora. If you’d like to generate your own corpus rather than use the one provided in the repo, you’ll want to use [`corpus_gen.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/corpus_gen.py). If you’d only like a specific part of our corpus, the method `get_subcorpus()` may be useful.  

## Citation

Cite the project using either the short or long form:

* Michael Scott Asato Cuthbert, et al., *Computational Reading of Gender in Novels, 1770–1922* (2019) <http://gendernovels.digitalhumanitiesmit.org>.

* Michael Scott Asato Cuthbert, Lisa Tagliaferri, Stephan Risi, Ife Ademolu-Odeneye, Dina Atia, Elena Boal, Emily Caragay, Susannah Chen, Alena Culbertson, Howard DaCosta, Mingfei Duan, Maritza Gallegos, Assel Ismoldayeva, Elsa Itambo, Michelle Li, Kelsey Merrill, Charlotte Minsky, Keith Murray, Carol Pan, Isaac Redlon, Shobita Sundaram, Felix Tran, Kate Xu, Derek Yen, Samantha York, Sophia Zhi, *Computational Reading of Gender in Novels, 1770–1922: The Gender/Novels Project* (2019) <http://gendernovels.digitalhumanitiesmit.org> and <https://github.com/dhmit/gender_novels>

*This document was prepared by the MIT Digital Humanities Lab.*

Copyright © 2018, [MIT Programs in Digital Humanities](https://digitalhumanities.mit.edu/). Released under the [BSD license](https://github.com/dhmit/gender_novels/blob/master/LICENSE).
Some included texts might not be out of copyright in all jurisdictions of the world.
