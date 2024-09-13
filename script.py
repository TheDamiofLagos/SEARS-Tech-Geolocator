from geopy.geocoders import Nominatim

def get_address(lat, lon):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapi")
    
    # Create a string with latitude and longitude
    location = geolocator.reverse((lat, lon), language='en')
    
    # Return the address if found
    if location:
        return location.address
    else:
        return "Address not found"

# Example usage
latitude = 6.5244
longitude = 3.3792

address = get_address(latitude, longitude)
print("Address:", address)
