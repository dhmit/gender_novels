# Grammar Analysis

We have implemented a function that outputs all the words that follows a specific keyword in a given novel. Then, these words are sorted by part of speech, which provides us with an opportunity to run analysis on the usage of various parts of speech with gendered pronouns. We have also included a function that gets the frequencies of several user-selected keywords.

The text of the novel has been processed so that only the sentences that contain gendered 
pronouns (he, she, him, his) are considered. For each of these sentences, a syntactic dependency 
tree is produced. The dependency tree contains information about the relationships between pairs 
of word in the sentence. This gave the opportunity to analyse the novels on a deeper level because we were able extract information not just from the individual word but also from the way they are positioned in the sentences. Here is an example of a dependency tree for the sentence _"Bills on ports and immigration were submitted by Senator Brownback, Republican of Kansas"_:

![Sentence Diagram](/static/markdowns/images/sentence_diagram.png "Sentence Diagram")

The information from the dependency tree was used to identify how many times male and female 
pronouns act as an active agent in the sentence versus how many time they act as a passive agent.
 It turned that often time male pronouns serve as active agents more frequently than female pronouns. 
 
 For example, in Louisa May Alcott’s _Little Men: Life at Plumfield with Jo's Boys_, male pronouns 
 appeared as an active agent 1260 times and female pronouns appeared as an active agent just 581 times.
The other piece of information that was extracted from the dependency trees is the adjectives and the verbs that are encountered with female versus male pronouns. The set of adjectives that are used with female pronouns vastly differs from the set of pronouns that are used with male adjectives.
