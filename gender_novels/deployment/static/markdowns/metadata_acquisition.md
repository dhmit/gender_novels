
# Metadata Acquisition

## About Metadata

Metadata is defined as "data about data."  In our case, metadata refers to additional data about our novels aside from the stories within them.  While acquiring metadata doesn't involve any natural language processing, this data is still very important for a variety of purposes.  For example, metadata is very important to analysis.  

#### Analysis Metadata
 - Author
 - Title
 - Publication date
 - Publication country
 - Author gender
 - Project Gutenberg-defined subjects

You can see that having the publication date would be useful for doing analysis of how literature changes over time, or how having the author gender would be useful for comparing how male and female authors represent their characters.  This kind of information would often be difficult or impossible to determine simply by analyzing the text.  

#### Filtering Metadata
 - Publication date
 - Copyright status
 - Language
 - Translation status
 - Project Gutenberg-defined subjects

These metadata are important for keeping the corpus clean and making sure only desired novels are included.  For example, we don't want any novels in Chinese.  However, not all of this metadata is actually saved by us--there's no reason to keep track of novel languages if we expect to only keep those that are in English.  

There's also some metadata that we associate with the books to make them easy to access and process but which aren't directly connected with analysis or filtering.  

#### Additional Metadata
 - Gutenberg ID
 - Corpus Name
 - Notes

## Metadata Sources
Where do we get metadata?  

### Project Gutenberg
The source for our novels has some important metadata already.  This includes the author, title, language, copyright status, and a convenient ID numbering system, and can be trusted to be generally reliable.  

The metadata on Project Gutenberg is stored in a single giant RDF file.  To handle this rather difficult file type, we used the [Gutenberg module](https://github.com/c-w/gutenberg).  Processing can take several hours, but it only needs to be done once on the machine that acquires the metadata.  Then getting the metadata is as easy as 

    get_metadata('title', 2701)

Unfortunately, Project Gutenberg doesn't provide important metadata like the publication date, so we need to look elsewhere.  But the author and title are important for looking up books in other databases.  

### Wikidata
Against the advice of high school teachers everywhere, we turned to Wikidata for information.  Wikidata has page ID's, and "claims" that define certain properties which also have ID's.  For example, `P2067` is the claim ID for mass.  `P2067` for page `Q402` is `125,260,000,000±210,000,000 electronvolt`, and `P2067` for page `Q22686` is `120 kilogram`.  (The former is the [Higgs boson](https://www.wikidata.org/wiki/Q402), the latter is [the US president](https://www.wikidata.org/wiki/Q22686)).  Using the [pywikibot](https://github.com/wikimedia/pywikibot) module, and a known claim ID, one can fairly simply access the information for a page.  

    site = pywikibot.Site("en", "wikipedia")
    page = pywikibot.Page(site, title)
    item = pywikibot.ItemPage.fromPage(page)
    dictionary = item.get()
    clm_dict = dictionary["claims"]
    clm_list = clm_dict["P577"] # publication date
    year = None
    for clm in clm_list:
	    clm_trgt = clm.getTarget()
    year = clm_trgt.year

The only catch is that if the value of a claim is another thing on Wikidata, you get the page ID back, not the name.  This means you have to either match the ID to the page title or go look up the name from Wikidata.  

The main issue with Wikidata is that although it contains [many](https://www.wikidata.org/wiki/Q18614236) [random](https://www.wikidata.org/wiki/Q15613810) [things](https://www.wikidata.org/wiki/Q970550), it doesn't contain many of the more obscure books.  Unfortunately, working with the Library of Congress and WorldCat API's was difficult, so we were unable to incorporate them into our metadata acquisition before the deadline.  [(Read more about that here).](url to Susanna's write-up)  However, there are some tricks to patch up those holes: 

### From the Text

There are a couple things that can be extracted from the text.  For example, most books have a copyright statement that goes like `COPYRIGHT. 1845`.  Using a regular expression, it's possible to get a lot of publication dates from the copyright statements.  

One can also usually be fairly sure that an author named "Mary Istabal" is probably female.  Using the [gender-guesser](https://pypi.org/project/gender-guesser/) module, we automated this process for cases where we couldn't find the author on Wikidata.  

## Generating the Metadata

Because some metadata is needed to filter out the books, we decided to generate the corpus and metadata at the same time.  [(Read more about generating the corpus here.)](Keith/Ife's writeup(s))  

To generate the corpus, we loop through every single Gutenberg ID number from zero to 70,000.  With each ID number, the book is first tested to see if it meets our [requirements](link to our definition of novel).  Then the metadata is acquired and written to a CSV file.  

	if (not is_valid_novel_gutenberg(gutenberg_id)):
		print("Not a novel")
		continue
	novel_metadata = get_gutenberg_metadata_for_single_novel(gutenberg_id)
	write_metadata(novel_metadata)
	...
	with open(Path(BASE_PATH, 'corpora', 'gutenberg', 'texts', f'{gutenberg_id}.txt'),
		mode='w', encoding='utf-8') as outfile:
		outfile.write(text_clean)
		number_books += 1

In the process of generating the corpus, we found that we had more than enough novels.  So greater emphasis was put on ensuring that included books were valid novels, even if it led to the exclusion of some legitimate novels.  We checked novels for 

 - Language and copyright status  using the gutenberg module
 - Certain keywords in the Gutenberg-defined subjects that indicated nonfiction or periodicals, like `correspondence`.  All novels had to contain the word `fiction` in their subject categories.  
 - Publication dates between 1770 and 1922
 - Certain phrases in the titles like `Index of the Project Gutenberg Works of`...
 - Indications that the text was a translation, like the presence of the string `Translator: ` in the text
 - The length of the text: all novels had to be between 140000 and [9609000](http://www.guinnessworldrecords.com/world-records/longest-novel) characters.  

For the methods that actually acquired the metadata, we used a process like this:

	date = get_publication_date_from_copyright_certain(novel_text)
	if date:
		return date
	else:
		date = get_publication_date_wikidata(author, title)
	if not date:
		date = get_publication_date_from_copyright_uncertain(novel_text)
	return date

Essentially, we would first try to get metadata from the most reliable source (in this case, the book itself), and if that failed we would try every method from most reliable to least reliable in turn, before giving up.  (For example, if the Library of Congress metadata acquisition was implemented, it would take first precedence).  

In several hours with a good computer it is possible to go through all the books from Project Gutenberg and generate a corpus with metadata.  

### A possible improvement

The `is_valid_novel` function needs to look up the publication date, so it calls `get_publication_date`.  Let's say `get_publication_date` manages to get the date from Wikidata, but it still loads the novel's text by `get_novel_text_gutenberg` for the `get_publication_date_from_copyright` function.  Then later, when evaluating the text, `is_valid_novel`calls `get_novel_text_gutenberg` again to check the length.  Then, once all that is done, `get_publication_date_from_copyright` gets called again to fill in the metadata field for the publication date, which once again calls `get_novel_text_gutenberg` and also `get_publication_date_wikidata`...  Each loop we call many functions more than once, and this happens roughly 50,000 times.  

A more efficient way to do this would be to cache all the already-found metadata and novel text into a dict that would be passed to the functions.  If a value was already in the dict, then there would be no need to find it again, and all these redundant function calls could be avoided.  

But there wasn't time to restructure all the code, and as it is the code is functional and runs in a reasonable amount of time.  So maybe next time?

[Check out the code on GitHub](https://github.com/dhmit/gender_novels/blob/master/gender_novels/corpus_gen.py).
