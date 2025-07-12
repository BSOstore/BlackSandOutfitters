from flask import Flask, render_template, request, redirect, url_for
from utils.storage import load_sites, save_sites
import csv
import os
from datetime import datetime


app = Flask(__name__, template_folder='templates')

# ----- HOME PAGE -----
@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    return render_template("index.html")

# ----- FAQ PAGE -----
@app.route("/faq")
def faq():
    return render_template("faq.html")

# ----- TUTORIAL PAGE -----
@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

# ----- UPGRADE PAGE -----
@app.route("/upgrade")
def upgrade():
    return render_template("upgrade.html")

# ----- ABOUT PAGE -----
@app.route("/about")
def about():
    return render_template("about.html")

# ----- CONTACT PAGE -----
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        email = request.form.get('email')
        file_path = os.path.join("data", "messages.csv")

        # Create file with header if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Email", "Subject", "Message"])

        # Append new message
        with open(file_path, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, email, subject, message])

        return redirect(url_for("index"))  # Make sure your home route is named 'index'

    return render_template("contact.html")



# ----- MAP PAGE -----
@app.route("/map", methods=["GET", "POST"])
def map_view():
    sites = load_sites()

    if request.method == "POST":
        new_site = {
            "name": request.form.get("site_name"),
            "lat": float(request.form.get("latitude")),
            "lon": float(request.form.get("longitude")),
            "notes": request.form.get("notes")
        }
        sites.append(new_site)
        save_sites(sites)
        return redirect(url_for("map_view"))

    # pick the *currently selected* site for Guide Me
    # (for now just use the first site)
    if sites:
        target_lat = sites[0]["lat"]
        target_lng = sites[0]["lon"]
    else:
        target_lat = target_lng = None   # or some default

    return render_template(
        "map.html",
        sites=sites,
        target_lat=target_lat,
        target_lng=target_lng
    )

# ----- ROI PAGE -----
@app.route('/roi', methods=['GET', 'POST'])
def roi():
    if request.method == 'POST':
        try:
            fuel = float(request.form.get('fuel', 0) or 0)
            food = float(request.form.get('food', 0) or 0)
            time = float(request.form.get('time', 0) or 0)
            misc = float(request.form.get('misc', 0) or 0)
            gold_amount = float(request.form.get('gold_amount', 0) or 0)
            gold_value = float(request.form.get('gold_value', 96.45) or 96.45)

            total_cost = fuel + food + time + misc
            total_gold_worth = gold_amount * gold_value
            roi_value = total_gold_worth - total_cost
        except ValueError:
            total_cost = total_gold_worth = roi_value = None

        return render_template(
            'roi.html',
            fuel=fuel,
            food=food,
            time=time,
            misc=misc,
            gold_amount=gold_amount,
            gold_value=gold_value,
            total_cost=total_cost,
            total_gold_worth=total_gold_worth,
            roi=roi_value
        )

    #❗ This GET branch must include the default values
    return render_template(
        'roi.html',
        fuel=None,
        food=None,
        time=None,
        misc=None,
        gold_amount=None,
        gold_value=96.45,
        total_cost=None,
        total_gold_worth=None,
        roi=None
    )

    # GET request fallback
    return render_template('roi.html')

from flask import request, jsonify

@app.route("/remove_pin", methods=["POST"])
def remove_pin_json():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")

    import os
    import json

    sites_file = os.path.join("data", "sites.json")

    try:
        with open(sites_file, "r") as f:
            sites = json.load(f)

        # Remove matching pin (safe float comparison)
        sites = [
            s for s in sites if not (
                round(float(s.get("lat", 0)), 6) == round(float(lat), 6) and
                round(float(s.get("lon", 0)), 6) == round(float(lon), 6)
            )
        ]

        with open(sites_file, "w") as f:
            json.dump(sites, f, indent=2)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500




import json
from flask import request, jsonify

# Adjust path if needed
SITES_FILE = "sites.json"

@app.route("/remove_pin", methods=["POST"])
def remove_pin():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")

    try:
        # Load existing sites
        with open(SITES_FILE, "r") as f:
            sites = json.load(f)

        # Remove the matching pin (float-safe comparison)
        sites = [s for s in sites if not (
            round(float(s.get("lat", 0)), 6) == round(float(lat), 6) and
            round(float(s.get("lon", 0)), 6) == round(float(lon), 6)
        )]

        # Write back to file
        with open(SITES_FILE, "w") as f:
            json.dump(sites, f, indent=2)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#BETA TEST SUBMISSION
from flask import Flask, request, redirect, url_for, render_template
import csv
import os


@app.route('/beta')
def beta():
    return render_template('beta.html')

from datetime import datetime  # ✅ Only use this one


@app.route("/submit-beta", methods=["POST"])
def submit_beta():
    last = request.form["last-name"]
    first = request.form["first-name"]
    state = request.form["state"]
    city = request.form["city"]
    age = request.form["age"]
    email = request.form["email"]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_file = os.path.join("data", "beta_testers.csv")
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Last Name', 'First Name', 'State', 'City', 'Age', 'Email'])

        writer.writerow([timestamp, last, first, state, city, age, email])  # ✅ No duplicate timestamp assignment

    return redirect(url_for('index.html'))

app.config.update(
  MAIL_SERVER='smtp.gmail.com',
  MAIL_PORT=587,
  MAIL_USE_TLS=True,
  MAIL_USERNAME='bsobetatest@gmail.com', # your full Gmail address
  MAIL_PASSWORD='mwepqrwtavyekclk', # paste your app password here
  MAIL_DEFAULT_SENDER='bsobetatest@gmail.com'
  )

@app.route("/beta_quiz")
def beta_quiz():
    return render_template("beta_quiz.html")


@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    frequency = request.form["frequency"]
    experience = request.form["experience"]
    like = request.form["like"]
    dislike = request.form["dislike"]
    rating = request.form["rating"]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_file = os.path.join("data", "beta_quiz.csv")
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Frequency', 'Experience', 'Liked', 'Disliked', 'Rating'])
        writer.writerow([timestamp, frequency, experience, like, dislike, rating])

    return redirect(url_for('index'))

    

@app.route("/beta-rating")
def beta_rating():
    import csv

    csv_file = os.path.join("data", "beta_quiz.csv")
    ratings = []

    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if "Rating" in row:
                    try:
                        ratings.append(int(row["Rating"]))
                    except ValueError:
                        pass  # skip rows with invalid rating
    except FileNotFoundError:
        ratings = []

    average = round(sum(ratings) / len(ratings), 2) if ratings else "No ratings yet"

    return render_template("beta_rating.html", average=average, count=len(ratings))


# PRIVACY PAGE
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")






# ✅ Only ONE app.run block, at the very end
import os

if __name__ == "__main__":
    app.run(debug=True)

