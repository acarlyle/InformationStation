# Views to display all forms

from flask import render_template, jsonify
from json import load
import datetime
from app import app

# Helper Functions

# Get the next few years that users can choose from
def nextFiveYears():
    year = datetime.datetime.now().year
    return [year+i for i in range(0,5)]

# Data for Javascript

@app.route('/api/endorsements')
def getEndorsements():
    try:
        with open('app/data/endorsements.json') as file:
            return jsonify(load(file))
    except:
        return jsonify({"error": "Failed to get file"}) # TODO change this to a response object that has a 400-something error code

@app.route('/api/schools')
def getSchools():
    try:
        with open('app/data/schools.json') as file:
            return jsonify(load(file))
    except:
        return jsonify({"error": "Failed to get file"})

# Routing

# Index
@app.route('/')
def index():
    return render_template("index.html")
    
# Admin Dashboard...?
@app.route('/dashboard')
def dashboard():
    return "This will be the dashboard...later"

# Continuation Form
@app.route('/forms/continuation')
def continuationForm():
    # Reason for not continuing
    reasons = ['Financial','Grades','Study Abroad','Moving out of Area','Personal','No longer interested in teaching','Other']
    return render_template("forms/continuation.html",years=nextFiveYears(),reasons=reasons)

# Internship Form
@app.route('/forms/internship')
def internshipForm():
    return render_template("forms/internship.html")

# Admission Form
@app.route('/forms/admission')
def admissionForm():
    return render_template("forms/admission.html")