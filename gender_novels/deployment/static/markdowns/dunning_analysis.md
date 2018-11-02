# Dunning Analysis

 The code used for this analysis can be found in [dunning.py](https://github
.com/dhmit/gender_novels/blob/master/gender_novels/analysis/dunning.py) under the 
 analysis folder.

 The statistical model used to analyze the distinctiveness of words
 is called Dunning Log-Likelihood, and it calculates how distinct a word
 is in its in one corpus compared to another corpus. For example, it can
 be used to compare male authors to female authors or 19th century novels
 to 20th century novels. It is also a very effective way to analyze the 
 word usage of authors, as it returns words that are not only distinctive
 by sheer amount but show a clear significantly distinctive.
 This means that words with relatively low frequencies can still receive high 
 dunning scores when compared to the rest of the words in their respective
 corpus. The function dunn_individual_word applies the mathematical formula
 used in Dunning Log-Likelihood and returns a dunning value for that specific word.
 As inputs, it takes in the total amount of words in both counter objects,
 and it also takes in the total counts of the desired word in their respective counters.

 **How to Use dunning_total**
  
  All that is needed to run dunning\_total is two counter or dict objects (counter1
  and counter2), mapping words to the number of times they appear. 
  When the function is run, it will execute dunn\_individual_word on all of the common words 
  in both counters. It will then return a dictionary that maps each word to 
  a dict containing its dunning score as well as the counts and frequencies with which
  it appears in both corpora. The negative end of the spectrum denotes the distinctiveness
  of the word in counter1, while the positive end of the spectrum does the 
  same for counter2. 
