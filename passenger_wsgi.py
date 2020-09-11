import sys, os

sys.path.insert(0, os.path.dirname(__file__))
venvpath = '/absolute/path/to/virtual/environment/python/lib/python3.7/site-packages'
sys.path.insert(0, venvpath)

from hello_factory_app import app as application
