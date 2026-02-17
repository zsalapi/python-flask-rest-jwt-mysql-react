# Import necessary Flask and Flask-JWT-Extended modules.
from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity  # jwt_required: protection; get_jwt_identity: reads the logged-in user's ID from the token.
from app.api import bp
from models import db, User  # Database connection and User model.
from app.errors import error_response


# Endpoint to get all users.
@bp.route("/users", methods=["GET"])
def get_users():
    # Query all users.
    users = User.query.all()
    # Return the list of users in JSON format. The 'to_json' method ensures that the password is not included.
    return jsonify([user.to_json() for user in users])


# Endpoint to get a user by ID.
@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    # Find the user by ID.
    user = User.query.get(id)
    # If it doesn't exist, we return a 404 error.
    if user is None:
        return error_response(404)
    # Return their data as JSON.
    return jsonify(user.to_json())


# Endpoint to create a new user (registration).
@bp.route("/users", methods=["POST"])
def create_user():
    # Get the JSON data from the request.
    data = request.get_json()
    # Check if the required 'name' and 'password' fields have been provided.
    if not data or not data.get('name') or not data.get('password'):
        return error_response(400, "The 'name' and 'password' fields are required.")

    # Check if the username is already taken.
    if User.query.filter_by(name=data['name']).first():
        return error_response(400, "Username is already taken.")

    # Create a new User object with the name.
    new_user = User(name=data['name'])
    # Set the hashed password using the 'set_password' method.
    new_user.set_password(data['password'])
    # Add the new user to the database session.
    db.session.add(new_user)
    # Commit the changes.
    db.session.commit()

    # Create the response.
    response = jsonify(new_user.to_json())
    # Set the status code to 201 Created.
    response.status_code = 201
    # Add the URL of the new user to the response header.
    response.headers["Location"] = url_for("api.get_user", id=new_user.id)
    return response


# Endpoint to update a user's data.
@bp.route("/users/<int:id>", methods=["PUT"])
@jwt_required  # Only accessible by a logged-in user.
def update_user(id):
    # Get the logged-in user's ID from the token.
    current_user_id = get_jwt_identity()
    # Check if the user is trying to modify their own data.
    if id != current_user_id:
        # If not, we return a 403 Forbidden error.
        return error_response(403)

    # Query the user to be updated from the database.
    user = User.query.get(id)
    if user is None:
        return error_response(404)

    data = request.get_json()
    if not data:
        return error_response(400, "No data in request.")

    # If a new name is provided, and it's different from the old one, AND it's already taken, we throw an error.
    if 'name' in data and data['name'] != user.name and User.query.filter_by(name=data['name']).first():
        return error_response(400, "Username is already taken.")

    # Update the name if provided.
    user.name = data.get('name', user.name)
    # Update the password if provided.
    if 'password' in data:
        user.set_password(data['password'])

    # Commit the changes.
    db.session.commit()
    return jsonify(user.to_json())


# Endpoint to delete a user.
@bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required  # Only accessible by a logged-in user.
def delete_user(id):
    # Get the logged-in user's ID.
    current_user_id = get_jwt_identity()
    # Check if they are trying to delete their own account.
    if id != current_user_id:
        return error_response(403)

    # Query the user to be deleted.
    user = User.query.get(id)
    if user is None:
        return error_response(404)

    # Delete the user.
    db.session.delete(user)
    db.session.commit()
    # Indicate successful deletion with a 204 No Content response.
    return "", 204
