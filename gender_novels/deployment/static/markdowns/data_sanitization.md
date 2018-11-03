# Data Sanitization

To make sure the data is as accurate as possible, it is necessary to decide how books 
should be added and refined for analysis.

For example, books on Project Gutenberg include a section before the text of the work itself, the
 Boilerplate, which includes information about Project Gutenberg's license, the upload date, and 
 other information about the digital format. Because this text is in complete English sentences 
 but itself an addition to the work, we had to find a way to remove the Boilerplate. Though most 
 books on Gutenberg have a standardized Boilerplate, a significant portion are non-standard. To 
 address the Boilerplates, we used a function strip_headers() from the Gutenberg Cleanup module, 
 which has been created to remove different kinds of headers.
 
The other textual addition of note is the Table of Contents. Unlike Boilerplates, Tables of 
Contents are part of the original work and were not added in the digitization process; but like 
Boilerplates, Tables of Contents vary greatly in their form. Some use Arabic numerals to number 
chapters (1, 2, 3...), some use Roman numerals (I, II, III...), others use English numbers (ONE, 
TWO, THREE...). Some include page numbers, other exclude them; some have page numbers on the same
 line, others stagger lines; some introduce their Tables of Contents with a header, while others 
 have no headers. Some books lack Tables of Contents altogether.
 

No function already existed which would remove the Table of Contents. After long consideration 
of the problem and numerous attempts at creating a lightweight means of removing the Tables of 
Contents, we decided that any code intended to remove them would likely cause greater problems such
 as inadvertently removing important data. Since the Table of Contents is such a minor fraction 
 of the total work and does not include complete English sentences (save for the a few chapter 
 titles), we deemed that it was wiser to not attempt removing them.
 
As for deciding which books to include in the corpus, it is best to first define a novel.

In scholarly journals, novels are often defined in terms of length and several other important 
abstract concepts. These concepts included a book’s ability to “[reflect] reality in the society in which it arises” and “[restore] the human spirit” (Mahfouz and Sultan 46). Naturally, the more abstract concepts were impossible to code, so books were selected from the Gutenberg corpus mostly in terms of their length.

After the initial corpus had been established, updating the sample novels corpus for testing 
became very important. We developed a method which creates a smaller corpus from a given database
 based on a specified common characteristic. Additionally, we implemented a method which serves 
 to bring up a specified number of examples from the corpus that include a specified keyword or 
 phrase.

Sources

Mahfouz, Naguib, and Sabbar S. Sultan. “The Situation of the Novel.” World Literature Today, vol. 79, no. 2, 2005, pp. 46–47. JSTOR, JSTOR, www.jstor.org/stable/40158674
