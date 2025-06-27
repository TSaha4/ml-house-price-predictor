# Importing necessary modules from Flask and another Python file (util.py)
from flask import Flask, request, jsonify, render_template  # Added render_template to serve index.html
from flask_cors import CORS
import sys 
import os    # For getting port from environment variables (needed for Render)

"""
Flask	        Python web framework that allows you to create backend APIs
util.py	        Your helper file containing the ML model and functions
@app.route	    URL endpoints that the frontend can call
request.form	Data sent from the frontend form (used in local dev)
request.get_json()	Data sent via JS in JSON format (used in deployed version)
jsonify	        Converts Python dictionary to JSON format for the frontend
CORS header	    Allows your frontend (from another port or domain) to access backend
"""

# Add the current directory to Python path to find util.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import util  # This is a custom Python file you created for utility functions

# Create a Flask web application instance
# Use absolute paths to avoid issues with relative paths on Render
client_dir = os.path.join(os.path.dirname(current_dir), 'client')
# '__name__' helps Flask determine the root path
# Added static_folder and template_folder so Flask can serve HTML/JS/CSS
app = Flask(
    __name__,
    static_folder=os.path.join(client_dir, 'static'),        # JS and CSS are in client/
    template_folder=client_dir       # index.html is in client/
)
CORS(app)  # Enables Cross-Origin requests from frontend


# Load the trained model and data columns from saved files
util.load_saved_artifacts()

# Define a route (URL endpoint) to serve the homepage (index.html)
@app.route('/')
def home():
    return render_template("index.html")

# Define a route (URL endpoint) to get all available location names
@app.route('/api/get_location_names')
def get_location_names():
    # Get location names from util.py and send them as a JSON response
    response = jsonify({
        'locations': util.get_location_names()
    })

    # Allow any frontend (like HTML/JavaScript) to access this API (CORS)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# Define another route to predict house price, accepts POST requests only
@app.route('/api/predict_home_price', methods=['POST'])
def predict_home_price():
    # Extract JSON data sent from frontend JavaScript (script.js)
    data = request.get_json()

    # Extract individual values from the request
    total_sqft = float(data['total_sqft'])       # Area of the house
    location = data['location']                  # Location name
    bhk = int(data['bhk'])                       # Number of bedrooms
    bath = int(data['bath'])                     # Number of bathrooms

    # Call function from util.py to predict the price using the model
    estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

    # Send the predicted price back as a JSON response
    response = jsonify({
        'estimated_price': estimated_price
    })

    # Again, allow frontend to access this API (important for web apps)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

# This tells Python to run the app only if this script is executed directly
# Use a dynamic port assigned by Render, defaulting to 5000 locally
if __name__ == '__main__':
    print("Starting Flask server for House Price Prediction...")

    port = int(os.environ.get("PORT", 5000))  # Render provides a port via env variable
    app.run(host='0.0.0.0', port=port)        # 0.0.0.0 makes it accessible publicly
