

Usage
=====


**For the end user** several scripts are provided to use **from the command line**:

.. code-block:: bash

    $ to_isbn10 ISBN13

transforms an ISBN13 number to ISBN10.

.. code-block:: bash

    $ to_isbn13 ISBN10

transforms an ISBN10 number to ISBN13.

.. code-block:: bash

    $ isbn_info ISBN

gives you the *group identifier* of the ISBN.

.. code-block:: bash

    $ isbn_mask ISBN

*masks* (hyphenate) an ISBN (split it by identifiers).

.. code-block:: bash

    $ isbn_meta ISBN [wcat|goob|openl|merge] [bibtex|...] [YOUR_APIKEY_TO_SERVICE]

gives you the main metadata associated with the ISBN, ``goob`` uses the **Google Books service** (**no key is needed**),
and **is the default option** (you only have to enter, e.g. ``isbn_meta 9780321534965``),
``openl`` uses the **OpenLibrary.org** api (**no key is needed**).
You can enter API keys and
set preferences in the file ``isbntools.conf`` in your
``$HOME\.isbntools`` directory (UNIX). For Windows, you should look at
``%APPDATA%/isbntools/isbntools.conf``. The output can be formatted as ``bibtex``, ``csl`` (CSL-JSON),
``msword``, ``endnote``, ``refworks``, ``opf`` or ``json`` (BibJSON) bibliographic formats.


.. code-block:: bash

    $ isbn_editions ISBN

gives the collection of ISBNs that represent a given book (uses **Open Library** and **LibraryThing**).

.. code-block:: bash

    $ isbn_validate ISBN

validates ISBN10 and ISBN13.

.. code-block:: bash

    $ ... | isbn_stdin_validate

to use with *posix pipes* (e.g. ``cat FILE_WITH_ISBNs | isbn_stdin_validate``).

    **TIP** Suppose you want to extract the ISBN of a pdf eboook (MYEBOOK.pdf).
    Install pdfminer_ and then enter in a command line::

        $ pdf2txt.py -m 5 MYEBOOK.pdf | isbn_stdin_validate



.. code-block:: bash

    $ isbn_from_words "words from title and author name"

a *fuzzy* script that returns the *most probable* ISBN from a set of words!
(You can verify the result with ``isbn_meta``)!


.. code-block:: bash

    $ isbn_goom "words from title and author name" [bibtex|csl|opf|msword|endnote|refworks|json]

a script that returns from **Google Books multiple references**.


.. code-block:: bash

    $ isbn_doi ISBN

returns the doi's ISBN-A code of a given ISBN.


.. code-block:: bash

    $ isbn_ean13 ISBN

returns the EAN13 code of a given ISBN.


.. code-block:: console

    $ isbn_classify ISBN

returns the OCLC classifiers of a given ISBN.


.. code-block:: bash

    $ isbn_ren FILENAME

renames (using metadata) files in the **current directory** that have ISBNs in their
filename (e.g. ``isbn_ren 1783559284_book.epub``, ``isbn_ren "*.pdf"``).

    Enter ``isbn_ren`` to see many other options.

.. code-block:: bash

    $ isbntools

writes version and copyright notice and **checks if there are updates**.

With

.. code-block:: bash

    $ isbn_repl

you will get a REPL with history, autocompletion, fuzzy options,
redirection and access to the shell.

Following is a typical session:

.. code-block:: console

    $ isbn_repl

        Welcome to the isbntools 4.3.15 REPL.
        ** For help type 'help' or '?'
        ** To exit type 'exit' :)
        ** To run a shell command, type '!<shellcmnd>'
        ** Use '#' in place of the last ISBN

    $ isbn> ?

    Commands available (type ?<command> to get help):
    -------------------------------------------------
    BIBFORMATS  classify  desc     ean13     from_words  info  to_isbn10
    PROVIDERS   conf      doi      editions  goom        mask  to_isbn13
    audit       cover     doi2tex  exit      help        meta  validate

    $ isbn> meta 9780156001311 tex
    @book{9780156001311,
         title = {The Name Of The Rose},
        author = {Umberto Eco},
          isbn = {9780156001311},
          year = {1994},
     publisher = {Harcourt Brace}
    }
    $ isbn> meta 9780156001311 tex >>myreferences.bib
    $ isbn> !ls
    myreferences.bib
    $ isbn> desc #
    It is the year 1327. Franciscans in an Italian abbey are suspected of
    heresy, but Brother William of Baskerville’s investigation is suddenly
    overshadowed by seven bizarre deaths. Translated by William Weaver. A Helen
    and Kurt Wolff Book
    $ isbn> cover #
         thumbnail:  http://books.google.com/books/content?id=PVVyuD1UY1wC&printsec=frontcover&img=1&zoom=1
    smallThumbnail:  http://books.google.com/books/content?id=PVVyuD1UY1wC&printsec=frontcover&img=1&zoom=5
    $ isbn> PROVIDERS
    bnf  goob  loc  merge  openl  porbase
    $ isbn> exit
    bye



**Within REPL many of the operations are faster.**

Many more scripts could be written with the ``isbntools`` library,
using the methods for extraction, cleaning, validation and standardization of ISBNs.

Just for fun, suppose I want the *most spoken about* book with certain words in his title.
For a *quick-and-dirty solution*, enter the following code in a file
and save it as ``isbn_tmsa_book.py``.

.. code-block:: python

    #!/usr/bin/env python
    import sys
    from isbntools import *

    query = sys.argv[1].replace(' ', '+')
    isbn = isbn_from_words(query)

    print("The ISBN of the most `spoken-about` book with this title is %s" % isbn)
    print("")
    print("... and the book is:")
    print("")
    print(registry.bibformatters['labels'](meta(isbn)))

Then in a command line (in the same directory):

.. code-block:: console

    $ python isbn_tmsa_book.py 'noise'

In my case I get::


    The ISBN of the most `spoken-about` book with this title is 9780143105985

    ... and the book is:

    Type:      BOOK
    Title:     White Noise
    Author:    Don DeLillo
    ISBN:      9780670803736
    Year:      1985
    Publisher: Viking



Have fun!

.. _pdfminer: https://pypi.python.org/pypi/pdfminer
