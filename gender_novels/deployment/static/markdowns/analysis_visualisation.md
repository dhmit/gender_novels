# Analysis Visualizations Breakdown

All visualization specialists are tasked with finding a way to graph our data in a manner that is
aesthetically pleasing.

For the visualizations, it is important take massive amounts of data and distill it into a 
comparison of more specific values. From here, interesting trends pop up that can lend themselves 
to more ground-breaking discoveries.

From here, we have turned the data into human readable and aesthetically pleasing graphs. 
Depending on the dataset, we had to make a decision on what graph would best represent the given 
data, and even more importantly what graph would emphasize the trend that the Analysis team members 
have noted.

### Foundation

We worked primarily in [matplotlib](https://matplotlib.org/contents.html), [seaborn](http://seaborn.pydata.org/index.html), 
and [pandas](https://pandas.pydata.org/)
 python modules to get the resulting graphs of our analyses. Because one of the goals of this project is accessibility, the entire visualization subset group has used seaborn’s colorblind pallet for their graphs. Below are several examples of the graphs made using these modules.

## Example Visualizations

#### Figure A: *She/He Relative Frequencies by Author*

![bar graph of she/he relative frequencies](images/he_she_freq0.png “bar graph of she/he relative frequencies”)


Figure A is a double bar graph, and displays the relative frequencies of ‘he’ and ‘she’ pronouns by book and author. This graph is but one of a series of graphs, all of which display the statistics for only one author and one book at a time. In this graph, outliers can be quickly spotted; names often lend a hint as to the gender of the author, thus allowing the viewer to take even more information from this visualization.

#### Figure B: *Relative Frequency of Female Pronouns to Total Pronouns*

![box and whisker plot of female pronoun frequency by author gender](images/she_freq_by_author_gender_sample.png “box and whisker plot of female pronoun frequency by author gender”)

Figure B, unlike Figure A, does not work with individual author and instances. Rather, Figure B provides a neat and tidy summarization of all the books in the tested corpus. To lend equal weight to every frequency from every book, Carol uses a series of boxplots. Boxplots not only show the three medians of a set, they also demonstrate where an outlier exists in the set, and thus are the best possible choice for this sort of investigation.

