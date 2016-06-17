import json
import logging.config
import os

__author__ = 'elvijs'

BASEDIR = os.path.split(__file__)[0]

with open(os.path.join(BASEDIR, 'logging-settings.json')) as f:
    logging.config.dictConfig(json.loads(f.read()))
