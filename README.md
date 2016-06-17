```
workon chess
python runapp.py
```


# Future plans 

JavaScript generators:
- AngularSeed
- Yeoman

Heroku for hosting.

For the initial prototyping I'm exporting games from (codekiddy's OTB-HQ) .si4 format to pgn. This will make it easier to manipulate, but less efficient. The latter part is a problem for later on however.

Had to actually use SCID to port convert si4 to pgn. A real shortage of good info/modules in this area and then 
`iconv -t UTF-8 -f ISO-8859-15 OTB-HQ.pgn > out.pgn` to convert to utf-8.

Create the virtual environment with python3: 
`mkvirtualenv --python=/usr/bin/python3 chess`

Notes for self: 
- [Deployment using fab, nginx, gunicorn and flask](https://realpython.com/blog/python/kickstarting-flask-on-ubuntu-setup-and-deployment/)

Some interesting links:

- [A very sexy JS lib](http://ebemunk.github.io/chess-dataviz/)
- [A potentially useful python module for prototyping](https://pypi.python.org/pypi/python-chess)
- [A collection of resources on chess](https://chessprogramming.wikispaces.com/). Seems focused on writing chess engines.