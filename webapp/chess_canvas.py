__author__ = 'elvijs'

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('test.html', name=name)
