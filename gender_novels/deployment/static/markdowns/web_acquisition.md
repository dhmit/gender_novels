# Web-Based Data Acquisition

At the start of the project, there was a challenge to come up with the most effective way to get an 
adequate corpus of books for analysis. Towards the beginning, this meant arriving at 100 books as
quickly as possible, so the analysis team could begin work with a small sample set of novels. Due
to time constraints, we chose to do this manually. We assigned members of the data group letters 
of the alphabet to ensure there was no overlap in books stored, and everyone was tasked with 
finding 9 books. This exercise allowed us to realize the problems we would face when writing the 
code to scrape the larger corpora of books. These problems included insufficient metadata on 
Gutenberg - meaning we had to manually searching publication dates to check that books had been 
published in the proper time frame. We also had to manually check the type of writing. For 
instance, if it was poetry, non-fiction or written in a foreign language. This led to the 
realization that there was an inadequate definition of novel, and that we had to better define our 
parameters. After setting out the terms of the filter, we had to agree on a method for 
automatically generating the corpora, as manual downloads would be too slow as the project scaled.
There are many regulations around the use of scrapers to get data from websites, so careful 
consideration was necessary to avoid any issues we might face using scrapers. In the end, we 
used mirrors and rsync to download the data.
