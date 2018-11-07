# How to Use our Corpus API

We created two classes — Novel and Corpus — which are necessary for running many of the analysis 
functions we created. They would also be useful for running additional new analyses. A basic 
overview and some important methods for each class are provided here, but more complete 
documentation can be found in the novel.py and corpus.py files [here](https://github
.com/dhmit/gender_novels/tree/master/gender_novels).

## Novel
*****

A Novel object represents a single novel. It has attributes which represent aspects of its 
metadata, such as `author_gender` and `country_publication`. The methods of the Novel class 
include `get_wordcount_counter`, which gets the frequency of each word used in the novel; 
`find_quoted_text`, which finds quoted 
text such as dialogue; and `words_associated`, which finds all the words written before or after 
a certain word in the novel (such as words after "he" or "she").


## Corpus
*****

A Corpus object represents an entire corpus of novels and is essentially a list of Novel objects.
Some useful methods of Corpus include `subcorpus`, which generates a new Corpus constrained by a
specific criterion, such as only including novels published in the UK and `multi_filter`, which
does the same but for multiple criteria at once; and `get_novel`, which extracts a particular 
novel.

### Downloading the Corpus

The Gutenberg corpus has already been generated with the code in `corpus_gen.py`.  As the 
corpus is too large to be stored in GitHub, passing in `'gutenberg'` as the parameter into the 
`Corpus` constructor for the first time will give you a prompt asking whether you want to 
download the Gutenberg corpus.  Entering `y` will download the corpus onto your machine.  

You are of course welcome to generate your own version of the corpus by running `corpus_gen.py` 
(note that you will have to [install the gutenberg module](/info/install_gutenberg)).  If you'd 
like to make a pull request on `corpus_gen.py` and modify our online corpus, please contact 
Stephan Risi at [risi@stanford.edu](mailto:risi@stanford.edu).  
