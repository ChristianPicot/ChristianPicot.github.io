// Initialize the map

let lat = -34.6037;
let lng = -58.3816;

const map = L.map('map').setView([lat, lng], 20); // 13 is the zoom level

// Add a tile layer (choose a map provider)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    function(position) {
      lat = position.coords.latitude;
      lng = position.coords.longitude;
      console.log("HOLA");
      map.setView([lat, lng], 16);
    },
    function(error) {
      console.error("Error getting user's location:", error);
      // Handle location access denied or other errors
      // For example, display an error message to the user
      // alert("Unable to access your location. Please check your browser settings.");
    }
  );
} else {
  console.error("Geolocation is not supported by this browser.");
}



// Add the locate control to the map
// L.control.locate({
//     setView: true, // Automatically zoom and center the map on the user's location
//     maxZoom: 16 // Maximum zoom level when locating the user
// }).addTo(map);

let busMarkers = {}; // Object to store bus markers

function updateBusPositions() {
    //fetch('https://paicot.pythonanywhere.com/bondis/') // Replace with your API endpoint
    fetch('https://181.170.199.213/bondis/') // Replace with your API endpoint    
        .then(response => response.json())
        .then(data => {
            data.forEach(bus => {
                const busId = bus.id;
                const lat = bus.latitude;
                const lng = bus.longitude;
                const linea = bus.linea;
                const label = bus.vehicle._vehicle._label;
                const velocidad = bus.vehicle._position._speed;

                if (busMarkers[busId]) {
                    // Update existing marker position
                    busMarkers[busId].setLatLng([lat, lng]);
                } else {
                    // Create a new marker
                    busMarkers[busId] = L.marker([lat, lng]).addTo(map)
                    .bindPopup(`<b>ID bondi:</b> ${busId}<br>
                        <b>Linea:</b> ${linea}<br>
                        <b>Velocidad:</b> ${velocidad}<br>
                        <b>Interno:</b> ${label}<br>`
                    );

                    // Add a moving icon (optional)
                    var busIcon = L.icon({
                        iconUrl: `./colectivosPNG/bondi${linea}.png`, //'bondi59.png', // Replace with the path to your icon
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
setInterval(updateBusPositions, 5000); // 30000 milliseconds = 30 seconds