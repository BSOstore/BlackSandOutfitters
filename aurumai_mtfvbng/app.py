
from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

# Path to site and feedback storage
DATA_FILE = 'data/sites.json'
FEEDBACK_FILE = 'data/feedback_log.txt'

# Ensure data directory and file exist
os.makedirs('data', exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_site():
    site = {
        "name": request.form['name'],
        "lat": request.form['lat'],
        "lon": request.form['lon'],
        "notes": request.form['notes']
    }
    with open(DATA_FILE, 'r') as f:
        sites = json.load(f)
    sites.append(site)
    with open(DATA_FILE, 'w') as f:
        json.dump(sites, f, indent=2)
    return redirect('/')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback = {
        "timestamp": datetime.now().isoformat(),
        "ease": request.form['ease'],
        "accuracy": request.form['accuracy'],
        "ui": request.form['ui'],
        "comments": request.form['comments']
    }
    with open(FEEDBACK_FILE, 'a') as f:
        f.write(json.dumps(feedback) + '\n')
    return "<h3>Thanks for your feedback!</h3><p><a href='/'>Return to app</a></p>"

if __name__ == '__main__':
    app.run(debug=True)
