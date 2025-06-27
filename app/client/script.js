// This function retrieves the selected number of bathrooms from the radio buttons
function getBathValue() {
    // Get all radio buttons with the name "uiBathrooms"
    var bathRadios = document.getElementsByName("uiBathrooms");

    // Loop through the radio buttons to find which one is checked
    for (var i = 0; i < bathRadios.length; i++) {
        if (bathRadios[i].checked) {
            // Return the number value of the selected radio button
            return parseInt(bathRadios[i].value);
        }
    }

    // Return -1 if none is selected (indicates error)
    return -1;
}

// This function retrieves the selected number of BHKs (bedrooms) from the radio buttons
function getBHKValue() {
    // Get all radio buttons with the name "uiBHK"
    var bhkRadios = document.getElementsByName("uiBHK");

    // Loop through them to find the checked one
    for (var i = 0; i < bhkRadios.length; i++) {
        if (bhkRadios[i].checked) {
            return parseInt(bhkRadios[i].value);
        }
    }

    // Return -1 if none is selected
    return -1;
}

// This function is called when the "Estimate Price" button is clicked
function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");

    // Get values from form fields
    var sqft = document.getElementById("uiSqft");              // Area input
    var bhk = getBHKValue();                                   // Selected BHK value
    var bathrooms = getBathValue();                            // Selected bathroom value
    var location = document.getElementById("uiLocations");     // Selected location
    var estPrice = document.getElementById("uiEstimatedPrice");// Element to display result

    // Log input values for debugging in console
    console.log("Inputs:", sqft.value, bhk, bathrooms, location.value);

    // Backend endpoint (Flask API) URL
    // var url = "http://127.0.0.1:5000/predict_home_price";
    var url = "/api/predict_home_price"; // Use relative URL for production

    // Send a POST request to the Flask backend
    $.post(url, {
        total_sqft: parseFloat(sqft.value), // Convert input to number
        bhk: bhk,
        bath: bathrooms,
        location: location.value
    }, function(data, status) {
        // When response is received from backend
        if (data && data.estimated_price !== undefined) {
            // Display the predicted price in the browser
            estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakhs</h2>";
        } else {
            // Show error message if response is invalid
            estPrice.innerHTML = "<h2>Error fetching price</h2>";
        }

        // Log the status of the request (success/failure)
        console.log(status);
    });
}

// This function runs automatically when the page is loaded
function onPageLoad() {
    console.log("Document loaded");

    // URL to call Flask backend to get all available locations
    // var url = "http://127.0.0.1:5000/get_location_names";
    var url = "/api/get_location_names";

    // Send a GET request to fetch location names from backend
    $.get(url, function(data, status) {
        console.log("got response for get_location_names request");

        if (data) {
            // Get list of locations from response
            var locations = data.locations;

            // Clear any existing dropdown options
            $('#uiLocations').empty();

            // Add a default "Choose a location" option that is disabled
            $('#uiLocations').append(new Option("Choose a location", "", true, true));
            $('#uiLocations option:first').attr("disabled", true);

            // Add each location as an option in the dropdown
            for (var i in locations) {
                var opt = new Option(locations[i], locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });
}

// This will trigger when the page finishes loading
window.onload = onPageLoad;
