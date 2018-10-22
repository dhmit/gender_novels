# Gutenberg Mirror Sample
This directory contains a tiny part (11 books) of the Gutenberg mirror. 
The sample is used for testing.

To generate your own full mirror, create a gutenberg_mirro directory and run the following command 
from there:

``` 
rsync -av --include='*.txt' --include='*/' --exclude='*' aleph.gutenberg.org::gutenberg .

```

Once you have created your full mirror, adjust the `GUTENBERG_RSYNC_PATH` so it points to the 
directory of your mirror.
