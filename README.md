# Get started

If the initial setup is complete, then the following will do.

`workon chess`
`python runapp.py`

The current state of the project admits one to query chess games by their ECO codes,
select a "from" move and "to" move (e.g. moves 10 and 20),
and view two heatmaps:
 * one of pieces landing on squares, and
 * one of lapse time of pieces on squares.

# Future plans 

## Immediate future

* Develop a few stories around a few different openings. Use for example [365chess](https://www.365chess.com/eco.php) to pick out openings that I know something about.

* Understand how many games are rejected due to bad parsing.
Improve the parsing of moves. There are a lot of rejected games due to comments etc.
Move the landing heatmap to using the chess module and make sure we log parsing errors.
Then simply add handling for the common cases.
Need to ensure that we don't mess up colours etc in the process.
Should be easy however - a quick glance suggests it's mostly comments e.g. "{Game xyz}" and
move evaluations e.g. "Nf3!!".
The simplest approach is actually probably to use the chess module move parsing functionality.

## Long-term functionality thinking

### Better filtering
* Drill deeper into openings (do deeper ECO codes exist?)
* Look at specific players/decades/rating strengths.

### If computer-evaluations are added
* Understand common mistakes in openings - heatmap of landing moves that produce a swing in evaluation.

### If eventual outcomes are taken into account
* The differences in won vs lost games.

## Long-term performance optimisation thinking

Investigate the representation of a chessboard as an 8x8 matrix (or a set of 8x8 matrices).
If we can also represent the chess moves as matrices, then the task of "playing" out
a game and computing a histogram of piece locations becomes purely mathematical.
Hence we could use numpy to represent the board with potential speedups in computations.
Moreover, this could be GPU-parallelisable.

Note that this line of reasoning was inspired by [Lewis Stiller's Multilinear Algebra and Chess Endgames](http://cdn.preterhuman.net/texts/math/MSRI_Volumes/Games%20of%20No%20Chance/stiller.pdf).

## Client side and hosting improvements

### JavaScript generators:
- AngularSeed
- Yeoman

### Heroku for hosting.

Notes for self:
- [Deployment using fab, nginx, gunicorn and flask](https://realpython.com/blog/python/kickstarting-flask-on-ubuntu-setup-and-deployment/)

# Notes on the current build

## Set up instructions

Download https://ebemunk.com/chess-dataviz/ and unzip in `webapp/static/js/chess-dataviz`.

```
mkvirtualenv --python=/usr/bin/python3 python3 -a `pwd`
workon chess
pip install -r requirements.txt
python runapp.py
```

For the initial prototyping I'm exporting games from (codekiddy's OTB-HQ) .si4 format to pgn. This will make it easier to manipulate, but less efficient. The latter part is a problem for later on however.

Had to actually use SCID to port convert si4 to pgn. A real shortage of good info/modules in this area and then 
`iconv -t UTF-8 -f ISO-8859-15 OTB-HQ.pgn > out.pgn` to convert to utf-8.