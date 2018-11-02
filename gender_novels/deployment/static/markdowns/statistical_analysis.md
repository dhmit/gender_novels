# Statistical Analysis

## Method

The statistical model used to analyze the distinctiveness of words is called Dunning Log-Likelihood, and it calculates how distinct a word is in its own corpus. This is a very effective way to analyze the word usage of authors, as it returns words that are not only distinctive by sheer amount but also significantly distinctive. This means that words with relatively low frequencies can still receive high dunning scores when compared to the rest of the words in their respective corpus. The function implemented applies the mathematical formula used in Dunning Log-Likelihood and returns a dunning value for that specific word. 

## Results

One of the analyses that used the dunning function was to find out the most distinctive words that male and female authors used throughout the 19th century. With female authors, words like “she” and “her” were used at an extremely high rate as compared to males, which is indicative of female authors having more important female characters in their novels. 
![](/static/markdowns/images/dunning_scores_pronouns.png "Pronoun Distributions")

Another thing that was interesting with female authors is that they used words like “Mr.” and “sir” much more than males, which shows how females typically addressed their male counterparts throughout this time. These words were not very prevalent amongst male authors, however, as males typically did not address each other with titles before. 

![](/static/markdowns/images/dunning_scores_words.png "Word Frequencies")
For the male authors, the most distinctive word by far was “the”. Although this is not particularly helpful in seeing how gender affected male writing styles, it shows that “he” and “his” are not the exact opposites of “she” and “her”. Another interesting finding with male authors was the prevalence of words that indicated status, with words like “count”, “sir”, and “duke” being some of the most distinctive words that were used by these male authors at the time.	
![](/static/markdowns/images/dunning_scores_adverbs.png "Adverb Frequencies")

![](/static/markdowns/images/dunning_scores_verbs.png "Verb Frequencies")
