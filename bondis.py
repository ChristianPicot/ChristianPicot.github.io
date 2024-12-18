import requests

def get_vehicle_locations(api_url):
    """
    Fetches vehicle locations from the given API URL.

    Args:
        api_url: The URL of the API endpoint.

    Returns:
        A list of dictionaries, where each dictionary represents a vehicle's location
        with keys 'latitude' and 'longitude'.
    """
    try:
        api_url = "https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id=XXXXXXXXXXXXXXX&client_secret=XXXXXXXXXXXXXXX&json=1&agency_id=84"
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
        return vehicle_locations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []



api_url = "https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositions?client_id=XXXXXXXXXXXXXXX&client_secret=XXXXXXXXXXXXXXX&json=1&agency_id=84"

print(get_vehicle_locations(api_url))