# Text Corpora
This folder contains all of the available text corpora.

Currently, each corpus is stored in its own folder.

## Available Corpora

#### Sample Novels
This is a dummy dataset to get us started. It consists of four
novels by Jane Austen, Nathaniel Hawthorne, Charles Dickens, and George Eliot.

## Data Organization
Each corpus folder should contain:
1. A csv file storing the metadata
2. All of the txt files in a separate "texts" subfolder

The metadata csv file should have columns for:
* author (format: "Last name, first name")
* date (year, in case of serial publication, year of first installment)
* title
* country_publication (United Kingdom should be split up into England, Wales, Scotland, and Northern Ireland)
* author_gender (male or female)
* filename (the name of the txt file)

