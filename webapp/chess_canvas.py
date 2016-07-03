from flask import request
import analysis
from analysis.heatmaps import get_landing_heatmap, get_landing_heatmap_in_parallel

__author__ = 'elvijs'

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('heatmap.html', name=name)


@app.route('/heatmap')
def get_heatmap():
    regex = request.args.get('regex')
    from_move = int(request.args.get('from'))
    to_move = int(request.args.get('to'))
    print("getting heatmap for opening {0}, between moves {1} and {2}".format(regex, from_move, to_move))
    analysis.from_move = from_move
    analysis.to_move = to_move
    heatmap = get_landing_heatmap_in_parallel(regex)
    return jsonify(**{'heatmap': heatmap})
