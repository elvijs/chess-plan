from flask import request
import analysis
from analysis.compute import get_landing_heatmap_in_parallel, get_lapse_heatmap_in_parallel
from flask import Flask, request, render_template, jsonify

__author__ = 'elvijs'

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
    print("getting heatmaps for opening {0}, between moves {1} and {2}".format(regex, from_move, to_move))
    analysis.from_move = from_move
    analysis.to_move = to_move
    print("getting lapse heatmap")
    lapse_heatmap = get_lapse_heatmap_in_parallel(regex)
    print("getting landing heatmap")
    landing_heatmap = get_landing_heatmap_in_parallel(regex)
    return jsonify(**{'lapse_heatmap': lapse_heatmap.state, 'landing_heatmap': landing_heatmap.state})
