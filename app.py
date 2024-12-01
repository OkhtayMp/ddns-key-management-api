from flask import Flask, request, jsonify  # type: ignore
import json
import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # Define the base directory

# Create the Flask application
app = Flask(__name__)

# Admin key for managing the system

ADMIN_KEY = os.getenv('ADMIN_KEY', '35c1dbca-c958-4dad-9f7d-a9fba8aa79e5')


# Path to the JSON data file
data_file = BASE_DIR / "data.json"

# Check if the file exists and initialize it with an empty list if necessary
if not data_file.exists():  # If the file does not exist
    with open(data_file, "w") as f:
        json.dump([], f)  # Write an empty list to the file
else:  # If the file exists
    with open(data_file, "r") as f:
        try:
            data = json.load(f)  # Attempt to load the data from the file
            if not data:  # If the data is empty
                data = []
                with open(data_file, "w") as f:
                    json.dump(data, f)  # Write an empty list to the file
        except json.JSONDecodeError:  # If there is an error parsing the file as JSON
            with open(data_file, "w") as f:
                json.dump([], f)  # Write an empty list to the file

# Load the data from the JSON file
def load_data():
    """Load the data from the data file."""
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return an empty list if the file is not found

# Save the provided data to the JSON file
def save_data(data):
    """Save the provided data to the data file."""
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)  # Write data to the file with indentation

# Endpoint to create a new key
@app.route("/create_key/<admin_key>", methods=["GET"])
def create_key(admin_key):
    """
    Create a new key if the provided admin key is correct.
    Args:
        admin_key (str): The admin key provided in the URL.
    Returns:
        JSON response with the new key or an error message.
    """
    if admin_key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403  # Return error if the admin key is incorrect

    # Generate a new UUID and add it to the data
    new_key = str(uuid.uuid4())
    data = load_data()
    data.append({"key": new_key, "ip": None})  # Add the new key with no IP address
    save_data(data)  # Save the updated data

    return jsonify({"key": new_key}), 201  # Return the new key in the response

# Endpoint to list all keys
@app.route("/list_key/<admin_key>", methods=["GET"])
def list_key(admin_key):
    """
    List all the keys and their associated IP addresses.
    Args:
        admin_key (str): The admin key provided in the URL.
    Returns:
        JSON response with the list of keys or an error message.
    """
    if admin_key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403  # Return error if the admin key is incorrect

    # Retrieve and return the list of keys
    data = load_data()
    keys = [{"key": entry["key"], "ip": entry["ip"]} for entry in data]

    return jsonify(keys), 200  # Return the list of keys

# Endpoint to remove a key
@app.route("/remove_key/<admin_key>", methods=["POST"])
def remove_key(admin_key):
    """
    Remove a specific key from the data.
    Args:
        admin_key (str): The admin key provided in the URL.
    Returns:
        JSON response confirming the removal or an error message.
    """
    if admin_key != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 403  # Return error if the admin key is incorrect

    # Retrieve the key to remove from the request body
    request_data = request.json
    key_to_remove = request_data.get("key")
    if not key_to_remove:
        return jsonify({"error": "Key is required"}), 400  # Return error if the key is not provided

    # Remove the key from the data
    data = load_data()
    data = [entry for entry in data if entry["key"] != key_to_remove]
    save_data(data)  # Save the updated data

    return jsonify({"message": f"Key {key_to_remove} removed"}), 200  # Confirm the removal

# Endpoint to add an IP address to a key
@app.route("/add_ip/<key>", methods=["POST"])
def add_ip(key):
    """
    Add an IP address to a specific key.
    Args:
        key (str): The key to which the IP will be added.
    Returns:
        JSON response with the updated key or an error message.
    """
    data = load_data()
    ip = request.json.get("ip")
    if not ip:
        return jsonify({"error": "IP is required"}), 400  # Return error if the IP is not provided

    # Update the key with the provided IP
    for entry in data:
        if entry["key"] == key:
            entry["ip"] = ip
            save_data(data)  # Save the updated data
            return jsonify(entry), 200  # Return the updated key

    return jsonify({"error": "Key not found"}), 404  # Return error if the key is not found

# Endpoint to get the IP address associated with a key
@app.route("/get_ip/<key>", methods=["GET"])
def get_ip(key):
    """
    Retrieve the IP address associated with a specific key.
    Args:
        key (str): The key for which the IP is requested.
    Returns:
        JSON response with the key and its IP or an error message.
    """
    data = load_data()
    for entry in data:
        if entry["key"] == key:
            return jsonify(entry), 200  # Return the key and its IP

    return jsonify({"error": "Key not found"}), 404  # Return error if the key is not found

# Main entry point for the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)  # Run the app in debug mode