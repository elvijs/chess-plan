from analysis.heatmaps import get_processed_heatmap_data

__author__ = 'elvijs'

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('test.html', name=name)


@app.route('/regex/<regex>')
def my_form_post(regex=None):
    print("form worked")
    heatmap = get_processed_heatmap_data(regex)
    return jsonify(**{'heatmap': heatmap})
