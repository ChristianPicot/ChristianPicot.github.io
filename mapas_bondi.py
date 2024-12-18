

1) what is L? when is L defined?
--> In Leaflet.js, the variable L is defined globally within the library's main JavaScript file
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

2) What do {s}, {z}, {x}, and {y} mean in 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'?


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {

    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

}).addTo(map);


placeholders
------------
--> {s}: Represents a subdomain. OSM uses multiple subdomains to distribute tile requests and avoid overloading any single server. It's replaced with an actual subdomain like a, b, or c at runtime.
--> {z}: Represents the zoom level
{x}: Represents the tile's X coordinate within the grid at the current zoom level.
{y}: Represents the tile's Y coordinate within the grid at the current zoom level.

--> L.tileLayer function uses the URL template to dynamically construct tile URLs based on the map's view and zoom level, fetching the necessary tiles to display the map.


map library (like Leaflet or Google Maps) to request the correct tiles as the user interacts with the map. 
a. When the map first loads, the map library determines which tiles are needed to display the initial view
b. then constructs URLs for these tiles based on the template and makes HTTP requests to fetch the tile images from a tile server.

+] Loading many small tiles is much faster than loading one large image
+] Browsers and Content Delivery Networks (CDNs) can cache tiles



1) En HTML crea el <div id="map"></div>
2) L.map(containerId, options): Creates a map instance and associates it with the HTML element identified by
const map = L.map('map').setView([-34.6037, -58.3816], 13); // 13 is the zoom level

3) L.tileLayer(urlTemplate, options): Creates a tile layer using a specified URL template and options.

tile layer: concept in web mapping, used to display large maps efficiently in a web browser. En vez de renderizar una imagen gigante!
Instead of loading a single, massive image of the entire map, the map is broken down into smaller, square images called "tiles." These tiles are then loaded and displayed as the user navigates and zooms the map


4) L.marker(latlng, options): Creates a marker at a given latitude and longitude with optional settings.



#
# Proveedores de mapas #
########################
https://www.mapbox.com/maps
OpenStreetMap (OSM)
Google Maps

######################
# Leaflet sirve para #
######################
display maps, add markers, popups, shapes, and other interactive elements.


https://leafletjs.com/

var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.marker([51.5, -0.09]).addTo(map)
    .bindPopup('A pretty CSS popup.<br> Easily customizable.')
    .openPopup();


######################
# backend en Node.js #
######################
const express = require('express');
const app = express();
const port = 3000; // Or any port you choose

app.get('/api/bus_positions', (req, res) => {
    // Make a request to your actual bus position API
    fetch('YOUR_ACTUAL_BUS_API_ENDPOINT')
        .then(apiResponse => apiResponse.json())
        .then(busData => {
            res.json(busData); // Send the data to the client
        })
        .catch(error => {
            console.error("Error fetching from external API:", error);
            res.status(500).json({ error: 'Failed to fetch bus positions' });
        });
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});


#############
# script.js #
#############
// Initialize the map
const map = L.map('map').setView([-34.6037, -58.3816], 13); // 13 is the zoom level

// Add a tile layer (choose a map provider)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let busMarkers = {}; // Object to store bus markers

function updateBusPositions() {
    fetch('https://rangos-libres-API-automation.telecentro.net.ar/bondis/') // Replace with your API endpoint
        .then(response => response.json())
        .then(data => {
            data.forEach(bus => {
                const busId = bus.id;
                const lat = bus.latitude;
                const lng = bus.longitude;

                if (busMarkers[busId]) {
                    // Update existing marker position
                    busMarkers[busId].setLatLng([lat, lng]);
                } else {
                    // Create a new marker
                    busMarkers[busId] = L.marker([lat, lng]).addTo(map).bindPopup(`Bus ID: ${busId}`);

                    // Add a moving icon (optional)
                    var busIcon = L.icon({
                        iconUrl: 'bondi59.png', // Replace with the path to your icon
                        iconSize: [32, 32], // Adjust icon size as needed
                        iconAnchor: [16, 16], // Adjust icon anchor as needed
                        popupAnchor: [0, -16]
                    });
                    busMarkers[busId].setIcon(busIcon);
                }
            });
        }).catch(error => {
            console.error("Error fetching bus positions:", error);
        });
}

// Initial update
updateBusPositions();

// Update positions every 30 seconds
setInterval(updateBusPositions, 300); // 30000 milliseconds = 30 seconds

#############
# mapa.html #
#############
<!DOCTYPE html>
<html>
<head>
    <title>No llega mas!!!</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        #map { height: 600px; } /* Adjust height as needed */
    </style>
</head>
<body>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="script.js"></script>
</body>
</html>


#########################
# backend API en python #
#########################
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

null=None
false=False
true=True

app = Flask(__name__)
CORS(app, origins=['*']) # esto me pemite recibir requests de distintos dominios sin tener que usar no-cors que despues el navegador no me permite utilizar sus resultados!


@app.route('/bondis/', methods=['GET'])
def get_vehicle_locations():
    """
    Fetches vehicle locations from the given API URL.

    Args:
        api_url: The URL of the API endpoint.

    Returns:
        A list of dictionaries, where each dictionary represents a vehicle's location
        with keys 'latitude' and 'longitude'.
    """
    try:
        api_url = "https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id=XXXXXX&client_secret=XXXXXXXXXX&json=1&agency_id=84"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        vehicle_locations = []
        for item in data["_entity"]:
            if "_vehicle" in item and "_position" in item["_vehicle"]:
                id = item["_vehicle"]["_vehicle"]["_id"]
                latitude = item["_vehicle"]["_position"]["_latitude"]
                longitude = item["_vehicle"]["_position"]["_longitude"]
                vehicle_locations.append({"latitude": latitude, "longitude": longitude, "id": id})
        return jsonify(vehicle_locations)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return jsonify([])
