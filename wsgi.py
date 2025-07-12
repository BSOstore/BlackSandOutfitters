import sys
import os
from flask import Flask

# Add the directory containing your app to the sys.path
sys.path.insert(0, '/home/bsofounder/mysite')

# Set the environment variable for Flask
os.environ['FLASK_APP'] = 'app.py'

# Import the app object from your Flask app file (app.py)
from app import app as application
