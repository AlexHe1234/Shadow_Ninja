import json
from datetime import datetime
from lib import create_app
from lib.orm import *
from gevent import pywsgi
import logging
from lib.engine import SearchEngine


if __name__ == '__main__':
    engine_instance = SearchEngine()
    engine_instance.run('shadow on the wall', 1000)
