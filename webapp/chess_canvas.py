from analysis.compute import HeatmapManager
from flask import Flask, request, render_template, jsonify

__author__ = 'elvijs'

app = Flask(__name__)

heatmap_manager = HeatmapManager()


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('heatmap.html', name=name)


@app.route('/heatmap')
def get_heatmap():
    regex = request.args.get('regex')
    from_move = int(request.args.get('from'))
    to_move = int(request.args.get('to'))
    print("getting heatmaps for opening {0}, "
          "between moves {1} and {2}".format(regex, from_move, to_move))
    print("getting lapse heatmap")
    lapse_heatmap = heatmap_manager.get_lapse_heatmap(regex, from_move, to_move)
    print("getting landing heatmap")
    landing_heatmap = heatmap_manager.get_landing_heatmap(regex, from_move, to_move)
    return jsonify(**{'lapse_heatmap': lapse_heatmap, 'landing_heatmap': landing_heatmap})
