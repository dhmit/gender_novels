# Gutenberg Mirror Sample
This directory contains a tiny part (11 books) of the Gutenberg mirror.
The sample is used for testing.

## Create Complete 4000 novel corpus.

To generate your own full mirror, create a gutenberg_mirror directory and run the following command
from there:

```
rsync -av --include='*.txt' --include='*/' --exclude='*' aleph.gutenberg.org::gutenberg .

```

The mirror will be about 41GB.

Once you have created your full mirror, adjust your environment settings for
`GUTENBERG_RSYNC_PATH` so it points to the directory of your mirror.  For instance,
on a Mac if you have placed a folder called "gutenberg_mirror" on your desktop and your
username is "bronte" you would run:

export GUTENBERG_RSYNC_PATH="/Users/bronte/Desktop/gutenberg_mirror"

Then run 'python -m gender_novels.corpus_gen' to generate the Gutenberg corpus
