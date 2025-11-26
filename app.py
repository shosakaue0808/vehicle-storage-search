from flask import Flask, request, jsonify
import json
from collections import defaultdict

app = Flask(__name__)


# Define the path to listing JSON file
file_path = 'listings.json' 

try:
    # Open the JSON file in read mode ('r')
    # The 'with' statement ensures the file is properly closed after use
    with open(file_path, 'r') as file:
        # Load the JSON data from the file into a Python object
        data = json.load(file)
    
    print("JSON data loaded successfully:")
    print(data)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{file_path}'. The file might be malformed.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Group listings by location_id
listing_by_location = defaultdict(list)
for listing in data:
    listing_by_location[listing["location_id"]].append(listing)
    print(listing) 

def expand_request(request_items):
    """
    Convert vehicle requests with quantities into a simple list of lengths.    
    :param request_items: list of dictinary of requested vehicles.
    example
    [
                {
                    "length": 10,
                    "quantity": 1
                },
                {
                    "length": 20,
                    "quantity": 2
                },
                {
                    "length": 25,
                    "quantity": 1
                }
    ]  
    """
    vehicles = []
    for item in request_items:
        length = item["length"]
        quantity = item["quantity"]
        for i in range (quantity):
            # add each length of vehicles with its quantity
            vehicles.append(length)
    # Sort longest vehicles first
    vehicles.sort(reverse=True)
    return vehicles

def can_fit_in_lane(vehicle_length, lane):
    """
    Check if a vehicle can fit in a lane based on its remaining length.
    
    Parameters:
        vehicle_length (int): Length of the vehicle.
        lane (dict): A lane within a storage listing, with remaining length.
    
    Returns:
        bool: True if the vehicle fits in the lane, False otherwise.
    """
    return lane["remaining_length"] >= vehicle_length

def place_vehicle_in_lane(vehicle_length, lane):
    """
    Place a vehicle in a lane, updating the remaining available length.
    
    Parameters:
        vehicle_length (int): Length of the vehicle.
        lane (dict): A lane within a storage listing, with remaining length.
    """
    lane["remaining_length"] -= vehicle_length

def check_storage_fitness(vehicles, listing):
    """
    Check if a storage listing can fit all the vehicles.
    
    Parameters:
        vehicles (list of int): List of vehicle lengths.
        listing (dict): A storage listing with width, length, and lanes information.
    
    Returns:
        bool: True if the storage fits all vehicles, False otherwise.
    """
    # Create lanes for the listing based on width / 10
    num_lanes = listing["width"] / 10  # Number of lanes based on width of the storage
    lanes = [{"remaining_length": listing["length"]} for _ in range(num_lanes)]

   # Iterate over each lane in the listing
    for lane in lanes:
        # Check if there are vehicles left to place
        if len(vehicles) == 0:
            return True  # All vehicles placed, some lanes are left unfilled (success)

        # Place vehicles into the lane until it's full or there are no more vehicles
        while len(vehicles) > 0 and can_fit_in_lane(vehicles[0], lane):
            place_vehicle_in_lane(vehicles.pop(0), lane)  # Place the vehicle and remove it from the list

    # After going through all the lanes, check if there are any remaining vehicles
    if len(vehicles) > 0:
        return False  # There are vehicles left, but no lanes left to place them

    return True  # All vehicles were placed successfully

def find_storages(vehicles, listings):
    valid_storage = []
    for listing in listings:
        if(check_storage_fitness(vehicles, listing)):
            valid_storage.append(listing)
    # Sort the valid_storage list by price_in_cents (ascending order)
    sorted_storage = sorted(valid_storage, key=lambda x: x['price_in_cents'])
    
    return sorted_storage


if __name__ == '__main__':
    app.run(debug=True)