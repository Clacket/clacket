# Initial Dataset

## Where it comes from
The base dataset used is the [Netflix Prize Dataset](http://academictorrents.com/details/9b13183dc4d60676b773c9e2cd6de5e5542cee9a), which we will use to train and test our model, with and without expansions (more features to each movie than just its name and year of release).

## Documentation
Documentation for the folder structure, usage license, and available features for the base dataset can be found in [this doc](https://drive.google.com/open?id=1Y8-AS24vKaMuszutCyM-rZ_IFINn1nNkTlU1zmUp3ng).

## Expansion
A [script](expand_movies.py) was written to retrieve more features per movie from the [Open Movie Database API](http://omdbapi.com). Those features are:
  - Genre(s) of the movie.
  - Actor(s).
  - Director(s).
  - Writer(s).
  - Language(s).
  - Country (or Countries).
  - Type (series, short, movie, etc).
  
We believe those features could make recommendations more accurate, but we are yet to test the accuracy of this assumption by comparing between recommendation accuracy with and without the extra features.

### Script Results
Out of 17770 titles, we were able to expand 9399 (52.8%) on the first try. The results were then stored in [expanded_movies.txt](expanded_movies.txt) in the following format (each line is a movie):

  ```Movie_Id|Title|Genres|Actors|Directors|Writers|Languages|Countries|Type```

Any field that can contain more than 1 entry (e.g. Genres) is comma-separated with no trailing comma.

Movies that could not be expanded were stored in the same format as movie_titles.txt (from the base dataset) in the file called [couldnt_expand.txt](couldnt_expand.txt).

### Script Usage
1. Download and extract the dataset into this folder (so files like movie_titles.txt are on top).
2. Run the script:

  ```bash
    $ chmod a+x expand_movies.py
    $ ./expand_movies.py
  ```
  Available options for the script:
  
  ```bash
    usage: expand_movies.py [-h] [-s] [-f] [-en] [-exp] [-fail]

    optional arguments:
      -h, --help           show this help message and exit
      -s, --start         Line number (starting from 1) of the first movie to
                           fetch.
      -f, --file          Path for the file that containsthe movie titles (every
                           line is a movie in the following format:
                           id,year_of_release,title
      -en, --encoding     Encoding of input file: UTF-8 or ISO-8859-1.
      -exp, --oexpanded   Path for the file where the expanded movies should be
                           output (does not have to exist).
      -fail, --ofailed    Path for the file where the failed entries should be
                           output (does not have to exist).
   ```
