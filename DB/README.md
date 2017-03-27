The database is compiled from [chesskid's 2.6m high quality otb games](http://codekiddy-chess.blogspot.co.uk/2015/11/15-million-chess-games-database.html).
There seems to be a real shortage of these.

At some point I should add a way to populate this from the web.
For simple tests, I currently only use the OTB-HQ games.

The following will come in handy:

`sudo apt-get install p7zip-full`

`7z x PACKAGE.7z`

This will populate the folder with a Scid DB (\*.sg4, \*.si4 and \*.sn4 files).
You can finally convert to PGN using sciDB (found on sourceforge)
