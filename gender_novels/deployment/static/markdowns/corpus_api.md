# How to Use our Corpus API [title in progress]

We created two classes — Novel and Corpus — which are necessary for running many of the analysis 
functions we created. They would also be useful for running additional new analyses. A basic 
overview and some important methods for each class are provided here, but more complete 
documentation can be found 
in [this is where we describe where to find documentation/just link to the github file?]

Novel
*****

A Novel object represents a single novel. It has attributes which represent aspects of its 
metadata, such as `author_gender` and `country_publication`. The methods of the Novel class 
include `get_wordcount_counter`, which gets the frequency of each word used in the novel; 
`find_quoted_text`, which finds quoted 
text such as dialogue; and `words_associated`, which finds all the words written before or after 
a certain word in the novel (such as words after "he" or "she").


Corpus
*****

A Corpus object represents an entire corpus of novels and is essentially a list of Novel objects.
 Some useful methods of Corpus include `subcorpus`, which generates a new Corpus constrained by a
  specific criterion, such as only including novels published in the UK and `multi_filter`, which
   does the same but for multiple criteria at once; and `get_novel`, which extracts a particular 
   novel.
