# Data Sanitation

To make sure the data is as accurate as possible, it is necessary to decide how books 
should be added and refined for analysis. For example, we needed to find a way to remove the tables of 
contents to prevent them from affecting our analysis. However, it soon became clear there was no 
standard way of formatting the table of context in the Gutenberg corpus and attempting to remove 
it would likely cause greater problems such as inadvertently removing important data. As for 
deciding which books to include in the corpus, it is best to first define a novel.

In scholarly journals, novels are often defined in terms of length and several other important 
abstract concepts. These concepts included a book’s ability to “[reflect] reality in the society in which it arises” and “[restore] the human spirit” (Mahfouz and Sultan 46). Naturally, the more abstract concepts were impossible to code, so books were selected from the Gutenberg corpus mostly in terms of their length.

After the initial corpus had been established, updating the sample novels corpus for testing  
became very important. We developed a method which creates a smaller corpus 
from a given database based on a specified common characteristic. Additionally, we implemented 
a method which serves to bring up a specified number of examples from the corpus that include a 
specified keyword or phrase.

Sources

Mahfouz, Naguib, and Sabbar S. Sultan. “The Situation of the Novel.” World Literature Today, vol. 79, no. 2, 2005, pp. 46–47. JSTOR, JSTOR, www.jstor.org/stable/40158674
