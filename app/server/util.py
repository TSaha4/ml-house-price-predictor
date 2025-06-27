# Importing required libraries
import json           # For reading the JSON file that contains column info
import pickle         # For loading the saved machine learning model
import numpy as np    # For creating and handling numerical arrays
import os             # NEW: To handle file paths dynamically

# Global variables to store model and data column info
__locations = None
__data_columns = None
__model = None

# Function to estimate the price based on input features
def get_estimated_price(location, sqft, bhk, bath):
    try: 
        # Get the index of the location in the list of data columns
        loc_index = __data_columns.index(location.lower())
    except:
        # If location is not found, set index to -1
        loc_index = -1

    # Create a zero array of the same length as the number of input features
    x = np.zeros(len(__data_columns))

    # Assign values to the input features
    x[0] = sqft     # First index is total area
    x[1] = bath     # Second index is number of bathrooms
    x[2] = bhk      # Third index is number of bedrooms

    # If location is found in data columns, set its index to 1 (one-hot encoding)
    if loc_index >= 0:
        x[loc_index] = 1

    # Predict the price using the loaded model and round to 2 decimal places
    return round(__model.predict([x])[0], 2)

# Function to return the list of location names
def get_location_names():
    return __locations

# Function to load the model and data columns from saved files
def load_saved_artifacts():
    print("Loading saved artifacts... start")

    # Use global to modify the global variables inside the function
    global __data_columns
    global __locations

    # Get the directory where this util.py file is located
    base_dir = os.path.dirname(__file__)

    # Load the list of data columns (including location names) from JSON file
    columns_path = os.path.join(base_dir, 'artifacts', 'columns.json')
    with open(columns_path, 'r') as f:
        __data_columns = json.load(f)['data_columns']  # Load data_columns key
        __locations = __data_columns[3:]               # First 3 are sqft, bath, bhk. Rest are locations

    global __model
    # Load the trained machine learning model from pickle file
    model_path = os.path.join(base_dir, 'artifacts', 'house_prediction.pickle')
    with open(model_path, 'rb') as f:
        __model = pickle.load(f)

    print("Loading saved artifacts... done")

# Test this module directly by running this file
if __name__ == '__main__':
    load_saved_artifacts()  # Load model and data
    print(get_location_names())  # Print available locations

    # Print sample predictions using test inputs
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))  # Unknown location
    print(get_estimated_price('Ejipura', 1000, 2, 2))   # Unknown location
