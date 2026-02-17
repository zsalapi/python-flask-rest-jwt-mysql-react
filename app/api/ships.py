# Import necessary Flask and Flask-JWT-Extended modules.
from flask import jsonify, request, url_for
# jsonify: creates a JSON response from a Python dict; request: incoming request data; url_for: generates a URL for an endpoint.
from flask_jwt_extended import jwt_required  # Decorator that requires a valid JWT token to access the endpoint.
from app.api import bp  # Our blueprint instance, on which we register the endpoints.
from models import db, Ship  # The database connection and the Ship model.
from app.errors import error_response  # Uniform error handler function.


# Endpoint to get all ships.
@bp.route("/ships", methods=["GET"])
def get_ships():
    # Query all records from the 'ships' table using SQLAlchemy.
    ships = Ship.query.all()
    # Convert the list of 'Ship' objects received into a JSON formatted list with the 'to_json' method, then return it.
    return jsonify([ship.to_json() for ship in ships])


# Endpoint to get a specific ship by identifier (ID).
@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    # Find the ship by ID. 'get' is a quick search for the primary key.
    ship = Ship.query.get(id)
    # If the ship is not found ('get' returns None), we send a 404 error.
    if ship is None:
        return error_response(404)
    # If found, return the ship's data in JSON format.
    return jsonify(ship.to_json())


# Endpoint to create a new ship.
@bp.route("/ships", methods=["POST"])
@jwt_required  # Only an authenticated user (with a valid access token) can access it.
def create_ship():
    # Get the JSON data from the request body.
    data = request.get_json()
    # If there is no data, we throw an error.
    if not data:
        return error_response(400, "No data in request.")

    # Check if the required fields have been provided.
    required_fields = ['model', 'ship_class']
    if not all(field in data for field in required_fields):
        return error_response(400, f"Missing required fields: {', '.join(required_fields)}")

    # Create a new 'Ship' object from the received data.
    new_ship = Ship(
        affiliation=data.get('affiliation'),
        category=data.get('category'),
        crew=data.get('crew'),
        length=data.get('length'),
        manufacturer=data.get('manufacturer'),
        model=data.get('model'),
        roles=data.get('roles'),
        ship_class=data.get('ship_class')
    )
    # Add the new object to the database "session".
    db.session.add(new_ship)
    # Commit the changes to the database.
    db.session.commit()

    # Return the data of the newly created ship as JSON.
    response = jsonify(new_ship.to_json())
    # Set the HTTP status code to 201 Created, indicating successful creation.
    response.status_code = 201
    # Add the URL of the new resource to the 'Location' header of the response.
    response.headers["Location"] = url_for("api.get_ship", id=new_ship.id)
    return response


# Endpoint to update an existing ship.
@bp.route("/ships/<int:id>", methods=["PUT"])
@jwt_required  # Only an authenticated user can access it.
def update_ship(id):
    # Find the ship to be updated by ID.
    ship = Ship.query.get(id)
    # If it doesn't exist, we return a 404 error.
    if ship is None:
        return error_response(404)

    # Get the JSON data from the request body.
    data = request.get_json()
    if not data:
        return error_response(400, "No data in request.")

    # Update the ship's attributes with the received data.
    # 'data.get(key, default_value)' is safer because if a key is missing, it keeps the existing value.
    ship.affiliation = data.get('affiliation', ship.affiliation)
    ship.category = data.get('category', ship.category)
    ship.crew = data.get('crew', ship.crew)
    ship.length = data.get('length', ship.length)
    ship.manufacturer = data.get('manufacturer', ship.manufacturer)
    ship.model = data.get('model', ship.model)
    ship.roles = data.get('roles', ship.roles)
    ship.ship_class = data.get('ship_class', ship.ship_class)

    # Commit the changes to the database.
    db.session.commit()
    # Return the updated ship's data.
    return jsonify(ship.to_json())


# Endpoint to delete a ship.
@bp.route("/ships/<int:id>", methods=["DELETE"])
@jwt_required  # Only an authenticated user can access it.
def delete_ship(id):
    # Find the ship to be deleted by ID.
    ship = Ship.query.get(id)
    # If it doesn't exist, we return a 404 error.
    if ship is None:
        return error_response(404)
    # Delete the object from the database "session".
    db.session.delete(ship)
    # Commit the change.
    db.session.commit()
    # On successful deletion, return a 204 No Content status code with an empty response.
    return "", 204
