# Contributing to Gender / Novels

This document, prepared by the members of the MIT Digital Humanities Lab, will guide you through contributing to the Gender / Novels project, from installation and usage through our coding style. 

As an open-source digital humanities project, we welcome contributions of code, documentation, and filed issues to iterate on this project and make it more expansive and applicable to a broad range of humanities researchers. 

## Installing Gender / Novels

The Gender / Novels project requires Python version 3.6 or later. If you need guidance on installing Python, review our [Python installation tutorial](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/setup/1_python_install.md). 

After you have the proper version of Python installed, ensure that you have Git set up so that you can work with this project via version control. You can read our [Installing and Setting Up Git tutorial](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/setup/2_git_install_setup.md) to get up and running with Git.

With Git installed, you should fork the `gender_novels` repository into your account. 

Open your local machine’s terminal and navigate to the directory where you would like the `gender_novels` files to be saved. For help in using the terminal/command line, review our [Introduction to the Command Line tutorial](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/command_line.md). Once you’re there, run the following:

```
git clone https://github.com/dhmit/gender_novels.git
```

This clones all files associated with the project to your directory. After that’s done, open your chosen IDE and navigate to the downloaded `gender_novels` files
- Navigate to `setup.py`
- Run `setup.py` — this installs the extra packages necessary to use our code

If you want to use the corpus generator in `corpus_gen.py,` you also need to install the [Gutenberg module](https://github.com/c-w/gutenberg). Follow the installation instructions in the [`README` file](https://github.com/c-w/gutenberg/blob/master/README.rst), and your setup is complete.

## Usage Guidelines

For anybody who wants to use our code, here’s a little outline of where everything is.
In the [`gender_novels/gender_novels`](https://github.com/dhmit/gender_novels/tree/master/gender_novels) folder, there are six folders:

1. [`analysis`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/analysis) — programming files focused on textual analysis and research write-ups, including data visualizations and conclusions
2. [`corpora`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/corpora) — metadata information on each book (including author, title, publication year, etc.), including sample data sets and instructions for generating a [Gutenberg mirror](https://github.com/dhmit/gender_novels/tree/master/gender_novels/corpora/gutenberg_mirror_sample)
3. [`deployment`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/deployment) — this directory holds programming files and assets related to the [Gender / Novels Flask website](http://gendernovels.digitalhumanitiesmit.org/)
4. [`pickle_data`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/pickle_data) — Pickled data for various analyses to avoid running time-consuming computation
5. [`testing`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/testing) — files for code tests
6. [`tutorials`](https://github.com/dhmit/gender_novels/tree/master/gender_novels/tutorials) — tutorials used by the lab to learn about various technical subjects needed to complete this project

For a user who’ll need some readily available methods for analyzing documents, the files you’ll most likely want are [`corpus.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/corpus.py) and [`novel.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/novel.py). These include methods used for loading and analyzing texts from the corpora. If you’d like to generate your own corpus rather than use the one provided in the repo, you’ll want to use [`corpus_gen.py`](https://github.com/dhmit/gender_novels/blob/master/gender_novels/corpus_gen.py). If you’d only like a specific part of our corpus, the method `get_subcorpus()` may be useful.  

## Contributing Guidelines

We welcome contributions in the form of code, documentation, and [filed issues](https://github.com/dhmit/gender_novels/issues). The purpose of the Gender / Novels project is to develop tools for literary analysis and research as it intersects with gender studies. If there’s a tool you wish existed to make your research more robust, feel free to contribute.

If you would like to contribute code, but are not sure where to begin, you can see what `TODO`s currently exist in the programming files or whether there are currently any open issues. Once you decide what you want to contribute, continue to read below in the next section.

If you would like to contribute documentation, please use Markdown. To learn more about Markdown, you can read our [Markdown tutorial](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/markdown.md). 

You can file an issue for a new feature or report a bug via our project’s [issues](https://github.com/dhmit/gender_novels/issues). This will start a conversation across the project’s community about how best to address the issue. To understand best practices for filing an issue, take a look at [GitHub’s Issues Guide](https://guides.github.com/features/issues/).

## Guidance on Code Contributions

Within the Digital Humanities Lab, testing and documentation are valued highly and are a priority. Towards this aim, we use the Python [doctest module](https://docs.python.org/3.7/library/doctest.html) throughout our code. For those who don’t know how to implement doctest, read [our Testing and doctest tutorial](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/testing_intro_doctest.ipynb). Every method, as part of the documentation, should include a doctest. These should be thorough and cover a wide variety of test cases and more importantly, these test cases should pass. If you’re having an issue with a particular doctest, leave a note in your pull request.

Please open pull requests whenever you change something. This way, we can create a dialogue about the changes quickly and make sure everybody is working on the most recent version of code.

Most of our code is written in Python, so if you need any advice on our in-house conventions, refer to the [Digital Humanities Lab Python Style Guide](https://github.com/dhmit/gender_novels/blob/master/gender_novels/tutorials/coding_style.md). If you have questions, don’t hesitate to ask!

## Community

Make sure you read the Code of Conduct before contributing. The Gender / Novels project is a space of collaboration and community; keep that in mind and maintain respect and professionalism throughout your interactions.

With that, we would like to thank you for all the awesome work you’re going to do.



