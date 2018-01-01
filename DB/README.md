# Masters DB

The database is compiled from [chesskid's 2.6m high quality otb games](https://sourceforge.net/projects/codekiddy-chess/files/Databases/Update4/).
There seems to be a real shortage of these.

The following will come in handy:

`sudo apt-get install p7zip-full`

`7z x PACKAGE.7z`

This will populate the folder with a Scid DB (\*.sg4, \*.si4 and \*.sn4 files).
You can finally convert to PGN using [sciDB](http://scidb.sourceforge.net/): open up the DB, then export to PGN and finally run the `import_and_store.py` script from this directory.

TODO: It would be great to automate this process, so that it's easier to restart the project. 

# Lichess

Note that [Lichess has made their games available]((here)[https://database.lichess.org/]) in a sensible PGN format.

Given the nice structure, the import is easy. Would be quite interesting to contrast top level online play insights versus those of masters play.