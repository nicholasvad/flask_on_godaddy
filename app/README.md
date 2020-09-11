# Setting Up a Simple Flask App on GoDaddy

These apps use the Setup Python App option within GoDaddy shared hosting.  This is based on Phusion Passenger, on Apache.

First you need to set up your domain and/or subdomain on cPanel.  It's easier if you have SSH set up, but it's not necessary.

### Then within 'Setup Python App'
1. Choose your Python version
1. Set you application root. I used `/home/username/my_app_directory`
1. Application url: as you have set up above.
1. Application entry point: `app` in my case.  This is the method which you want the `passenger_wsgi.py` file to load.
1. Passenger log file: wherever you want; `/home/username/logs/my_app.log`

## 1. Using a Basic Flask App
`passenger_wsgi.py` file\
This is created when you save the setup. I adapted it as follows:
```python
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
venvpath = '/absolute/path/to/virtual/environment/python/lib/python3.7/site-packages'
sys.path.insert(0, venvpath)

from hello_simple_app import app as application
```

The basic app file, `hello_simple_app.py`, is then straight from the Flask docs:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World online!'
```
Beware changes to these files when you stop and start the app. I took copies of these just in case restarting the Python app caused them to be replaced; it did happen somehow once.

When you create an app, GoDaddy creates a virtual environment. This is in the directory:\
`/home/username/virtualenv/my_app_directory/<your Python version>` \
Use this command to activate your virtual environment:\
```
$ source source /home/username/virtualenv/my_app_directory/3.7/bin/activate && cd /home/username/my_app_directory
```
I saved this as a function. Straight away I found that pip was a very old version, so I immediately updated it to the latest version with:
```
$ python -m pip install --upgrade pip
```
It is worth checking your Python version. 
You also need to install Flask.
```
$ python -V
$ pip install flask
```
When you create the app, it makes an `.htaccess` file. I needed to add the line to remove the directory index. When you stop the app in cPanel, it removes the top four lines it made.
```
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION BEGIN
PassengerAppRoot "/absolute/path/to/app"
PassengerBaseURI "/"
PassengerPython "/absolute/path/to/virtualenv/bin/file/3.7/bin/python"
PassengerAppLogFile "/absolute/path/to/logs/app.log"
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION END

# Turn off directory index if necessary
Options -Indexes
```
\
There is a special trick to restart the app from the command line if you have made changes, to save the risk of any of your files being overwritten when you stop and start the app within cPanel.  Simple `touch` the empty `restart.txt` file in the `tmp` directory:
```
$ touch tmp/restart.txt
```

## 2. Using the Factory Pattern
Revise `passenger_wsgi.py` to import from the file where your `app` module is.\
My `__init__.py` file, in the app folder, was:
```python
from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    @app.route('/')
    def hello():
        return 'Hello World revised!'

    return app
```
My module to create the app was:
```python
import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG') or 'cloud')
```
You can see how I have used a `config.py` file and a `.env` file.  I installed `python-dotenv`.
```
pip install python-dotenv
```

I hope that helps others, as well as being a reference for me.