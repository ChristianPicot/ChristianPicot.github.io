// Initialize the map
const map = L.map('map').setView([-34.6037, -58.3816], 13); // 13 is the zoom level

// Add a tile layer (choose a map provider)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let busMarkers = {}; // Object to store bus markers

function updateBusPositions() {
    fetch('https://paicot.pythonanywhere.com/bondis/') // Replace with your API endpoint
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


function updateBusPositionsNEW() {
    // fetch('https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id=XXXXX&client_secret=XXXXXXX&json=1&agency_id=84') // Replace with your API endpoint
    fetch('https://paicot.pythonanywhere.com/bondis/') // Replace with your API endpoint
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const busId = item["_vehicle"]["_vehicle"]["_id"]; //bus.id;
                const lat = item["_vehicle"]["_position"]["_latitude"]; //bus.latitude;
                const lng = item["_vehicle"]["_position"]["_longitude"]; //bus.longitude;

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